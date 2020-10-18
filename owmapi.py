# Copyright 2020, Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json
import time
from copy import deepcopy
from pyowm import OWM
from pyowm.webapi25.forecaster import Forecaster
from pyowm.webapi25.forecastparser import ForecastParser
from pyowm.webapi25.observationparser import ObservationParser
from requests import HTTPError, Response
from mycroft.api import Api
from mycroft.util.log import LOG

"""
    This skill uses the Open Weather Map API (https://openweathermap.org) and
    the PyOWM wrapper for it.  For more info, see:

    General info on PyOWM
    https://www.slideshare.net/csparpa/pyowm-my-first-open-source-project
    OWM doc for APIs used
        https://openweathermap.org/current - current
        https://openweathermap.org/forecast5 - three hour forecast
        https://openweathermap.org/forecast16 - daily forecasts
    PyOWM docs
        https://media.readthedocs.org/pdf/pyowm/latest/pyowm.pdf
"""

MINUTES = 60  # Minutes to seconds multiplier


class LocationNotFoundError(ValueError):
    pass


class OWMApi(Api):
    ''' Wrapper that defaults to the Mycroft cloud proxy so user's don't need
        to get their own OWM API keys '''

    def __init__(self):
        super(OWMApi, self).__init__("owm")
        self.owmlang = "en"
        self.encoding = "utf8"
        self.observation = ObservationParser()
        self.forecast = ForecastParser()
        self.query_cache = {}
        self.location_translations = {}

    @staticmethod
    def get_language(lang):
        """Convert language code to OWM format, if missing defaults to 'en'.

        OWM supports 31 languages, see https://openweathermap.org/current#multi

        Arguments:
            lang (String): Full language code eg "en-us"
        Returns:
            OWM compatible language code eg "en"        
        """

        owmlang = 'en'

        # some special cases
        if lang == 'zh-zn' or lang == 'zh_zn':
            return 'zh_zn'
        elif lang == 'zh-tw' or lang == 'zh_tw':
            return 'zh_tw'

        # special cases cont'd
        lang = lang.lower().split("-")
        lookup = {
            'sv': 'se',
            'cs': 'cz',
            'ko': 'kr',
            'lv': 'la',
            'uk': 'ua'
        }
        if lang[0] in lookup:
            return lookup[lang[0]]

        owmsupported = ['ar', 'bg', 'ca', 'cz', 'da', 'de', 'el', 'en', 'fa', 'fi',
                        'fr', 'gl', 'hr', 'hu', 'it', 'ja', 'kr', 'la', 'lt',
                        'mk', 'nl', 'pl', 'pt', 'ro', 'ru', 'se', 'sk', 'sl',
                        'es', 'tr', 'ua', 'vi']

        if lang[0] in owmsupported:
            owmlang = lang[0]
        if (len(lang) == 2):
            if lang[1] in owmsupported:
                owmlang = lang[1]
        return owmlang

    def _request(self, data):
        """ Caching the responses """
        req_hash = hash(json.dumps(data, sort_keys=True))
        cache = self.query_cache.get(req_hash, (0, None))
        # check for caches with more days data than requested
        if data['query'].get('cnt') and cache == (0, None):
            test_req_data = deepcopy(data)
            while test_req_data['query']['cnt'] < 16 and cache == (0, None):
                test_req_data['query']['cnt'] += 1
                test_hash = hash(json.dumps(test_req_data, sort_keys=True))
                test_cache = self.query_cache.get(test_hash, (0, None))
                if test_cache != (0, None):
                    cache = test_cache
        # Use cached response if value exists and was fetched within 15 min
        now = time.monotonic()
        if now > (cache[0] + 15 * MINUTES) or cache[1] is None:
            resp = super().request(data)
            # 404 returned as JSON-like string in some instances
            if isinstance(resp, str) and '{"cod":"404"' in resp:
                r = Response()
                r.status_code = 404
                raise HTTPError(resp, response=r)
            self.query_cache[req_hash] = (now, resp)
        else:
            LOG.debug('Using cached OWM Response from {}'.format(cache[0]))
            resp = cache[1]
        return resp

    def get_data(self, response):
        # Removing this breaks the Skill but I can't see where it's being used
        return response.text

    def _weather_at_location(self, name):
        if name == '':
            raise LocationNotFoundError('The location couldn\'t be found')

        q = {"q": name}
        try:
            data = self._request({
                "path": "/weather",
                "query": q
            })
            return self.observation.parse_JSON(data), name
        except HTTPError as e:
            if e.response.status_code == 404:
                name = ' '.join(name.split()[:-1])
                return self._weather_at_location(name)
            raise

    def weather_at_place(self, name, lat, lon):
        """Get current weather for specific location.

        If available, the latitude and longitude will be used to determine
        the location as this is more precise and cannot have duplicates.

        Arguments:
            name (String): name of location
            lat (Float): latitude
            lon (Float): longitude
        Returns:
            Observation instance
        """
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            if name in self.location_translations:
                name = self.location_translations[name]
            response, trans_name = self._weather_at_location(name)
            self.location_translations[name] = trans_name
            return response

        data = self._request({
            "path": "/weather",
            "query": q
        })
        return self.observation.parse_JSON(data)

    def three_hours_forecast(self, name, lat, lon):
        """Get 3 Hour Forecaster instance for specific location.

        If available, the latitude and longitude will be used to determine
        the location as this is more precise and cannot have duplicates.

        Arguments:
            name (String): name of location
            lat (Float): latitude
            lon (Float): longitude
        Returns:
            Forecaster instance or None if forecast data is not available for
            the specified location.
        """
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            if name in self.location_translations:
                name = self.location_translations[name]
            q = {"q": name}

        data = self._request({
            "path": "/forecast",
            "query": q
        })
        return self.to_forecast(data, "3h")

    def _daily_forecast_at_location(self, name, limit):
        if name in self.location_translations:
            name = self.location_translations[name]
        orig_name = name
        while name != '':
            try:
                q = {"q": name}
                if limit is not None:
                    q["cnt"] = limit
                data = self._request({
                    "path": "/forecast/daily",
                    "query": q
                })
                forecast = self.to_forecast(data, 'daily')
                self.location_translations[orig_name] = name
                return forecast
            except HTTPError as e:
                if e.response.status_code == 404:
                    # Remove last word in name
                    name = ' '.join(name.split()[:-1])

        raise LocationNotFoundError('The location couldn\'t be found')

    def daily_forecast(self, name, lat, lon, limit=None):
        """Get daily Forecaster instance for specific location.

        If available, the latitude and longitude will be used to determine
        the location as this is more precise and cannot have duplicates.

        Arguments:
            name (String): name of location
            lat (Float): latitude
            lon (Float): longitude
            limit (Int): maximum number of Weather items to be retrieved
                         Default is None which equates to no limit.
        Returns:
            Forecaster instance or None if forecast data is not available for
            the specified location.
        """
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            return self._daily_forecast_at_location(name, limit)

        if limit is not None:
            q["cnt"] = limit
        data = self._request({
            "path": "/forecast/daily",
            "query": q
        })
        return self.to_forecast(data, "daily")

    def to_forecast(self, data, interval):
        """Convert weather data to a Forecaster instance.

        Arguments:
            data (Obj): weather data to parse
            interval (String): granularity of the forecast - `3h` or 'daily'
        Returns:
            Forecaster instance or None
        """
        forecast = self.forecast.parse_JSON(data)
        if forecast is not None:
            forecast.set_interval(interval)
            return Forecaster(forecast)
        else:
            return None

    def set_OWM_language(self, lang):
        """Set the language and encoding.

        Certain OWM condition information is encoded using non-utf8
        encodings. If another language needs similar solution add them to the
        encodings dictionary.

        Arguments:
            lang (String): OWM compatible language code
        """
        self.owmlang = lang

        encodings = {
            'se': 'latin1'
        }
        self.encoding = encodings.get(lang, 'utf8')
