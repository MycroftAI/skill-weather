# Copyright 2017, Mycroft AI Inc.
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

import time
from datetime import datetime
from copy import copy
import json

import mycroft.audio
from adapt.intent import IntentBuilder
from multi_key_dict import multi_key_dict
from mycroft.dialog import DialogLoader
from mycroft.api import Api
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.format import nice_time
from mycroft.util.log import LOG
from mycroft.util.parse import extract_datetime
from mycroft.util.format import nice_number
from pyowm import OWM
from pyowm.webapi25.forecaster import Forecaster
from pyowm.webapi25.forecastparser import ForecastParser
from pyowm.webapi25.observationparser import ObservationParser
from requests import HTTPError

try:
    from mycroft.util.time import to_utc, to_local
except Exception:
    import pytz

MINUTES = 60 # Minutes to seconds multiplier

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
        """
        OWM supports 31 languages, see https://openweathermap.org/current#multi

        Convert language code to owm language, if missing use 'en'
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

        owmsupported = ['ar','bg','ca','cz','de','el','en','fa','fi','fr','gl',
                    'hr','hu','it','ja','kr','la','lt','mk','nl','pl','pt',
                    'ro','ru','se','sk','sl','es','tr','ua','vi']

        if lang[0] in owmsupported:
            owmlang = lang[0]
        if (len(lang)==2):
            if lang[1] in owmsupported:
                owmlang = lang[1]
        return owmlang


    def build_query(self, params):
        params.get("query").update({"lang": self.owmlang})
        return params.get("query")

    def request(self, data):
        """ Caching the responses """
        req_hash = hash(json.dumps(data, sort_keys=True))
        cache = self.query_cache.get(req_hash, (0, None))

        # Use cached response if recent and cached value exists
        now = time.monotonic()
        if now > (cache[0] + 15 * MINUTES) or cache[1] is None:
            resp = super().request(data)
            self.query_cache[req_hash] = (now, resp)
        else:
            LOG.debug('Using cached OWM Response from {}'.format(cache[0]))
            resp = cache[1]

        return resp

    def get_data(self, response):
        return response.text

    def weather_at_location(self, name):
        if name == '':
            raise ValueError

        q = {"q": name}
        try:
            data = self.request({
                "path": "/weather",
                "query": q
            })
            return self.observation.parse_JSON(data), name
        except HTTPError as e:
            if e.response.status_code == 404:
                name = ' '.join(name.split()[:-1])
                return self.weather_at_location(name)
            raise

    def weather_at_place(self, name, lat, lon):
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            if name in self.location_translations:
                name = self.location_translations[name]
            response, trans_name = self.weather_at_location(name)
            self.location_translations[name] = trans_name
            return response

        data = self.request({
            "path": "/weather",
            "query": q
        })
        return self.observation.parse_JSON(data)

    def three_hours_forecast(self, name, lat, lon):
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            if name in self.location_translations:
                name = self.location_translations[name]
            q = {"q": name}

        data = self.request({
            "path": "/forecast",
            "query": q
        })
        return self.to_forecast(data, "3h")

    def daily_forecast(self, name, lat, lon, limit=None):
        if lat and lon:
            q = {"lat": lat, "lon": lon}
        else:
            if name in self.location_translations:
                name = self.location_translations[name]
            q = {"q": name}

        if limit is not None:
            q["cnt"] = limit
        data = self.request({
            "path": "/forecast/daily",
            "query": q
        })
        return self.to_forecast(data, "daily")

    def to_forecast(self, data, interval):
        forecast = self.forecast.parse_JSON(data)
        if forecast is not None:
            forecast.set_interval(interval)
            return Forecaster(forecast)
        else:
            return None

    def set_OWM_language(self, lang):
        self.owmlang = lang

        # Certain OWM condition information is encoded using non-utf8
        # encodings. If another language needs similar solution add them to the
        # encodings dictionary
        encodings = {
            'se': 'latin1'
        }
        self.encoding = encodings.get(lang, 'utf8')


class WeatherSkill(MycroftSkill):
    def __init__(self):
        super().__init__("WeatherSkill")

        # Build a dictionary to translate OWM weather-conditions
        # codes into the Mycroft weather icon codes
        # (see https://openweathermap.org/weather-conditions)
        self.CODES = multi_key_dict()
        self.CODES['01d', '01n'] = 0                # clear
        self.CODES['02d', '02n', '03d', '03n'] = 1  # partly cloudy
        self.CODES['04d', '04n'] = 2                # cloudy
        self.CODES['09d', '09n'] = 3                # light rain
        self.CODES['10d', '10n'] = 4                # raining
        self.CODES['11d', '11n'] = 5                # stormy
        self.CODES['13d', '13n'] = 6                # snowing
        self.CODES['50d', '50n'] = 7                # windy/misty
        
        # Use Mycroft proxy if no private key provided
        self.settings["api_key"] = None
        self.settings["use_proxy"] = True

    def initialize(self):
        # TODO: Remove lat,lon parameters from the OWMApi()
        #       methods and implement _at_coords() versions
        #       instead to make the interfaces compatible
        #       again.
        #
        # if self.settings["api_key"] and not self.settings['use_proxy']):
        #     self.owm = OWM(self.settings["api_key"])
        # else:
        #     self.owm = OWMApi()
        self.owm = OWMApi()
        if self.owm:
            self.owm.set_OWM_language(lang=OWMApi.get_language(self.lang))
        
        try:
            self.mark2_forecast(self.__initialize_report(None))
        except Exception as e:
            LOG.warning('Could not prepare forecasts. ({})'.format(repr(e)))

        # Register for handling idle/resting screen
        msg_type = '{}.{}'.format(self.skill_id, 'idle')
        self.add_event(msg_type, self.handle_idle)
        self.add_event('mycroft.mark2.collect_idle',
                       self.handle_collect_request)

    def handle_collect_request(self, message):
        self.log.info('Registering idle screen')
        self.bus.emit(Message('mycroft.mark2.register_idle',
                              data={'name': 'Weather',
                                    'id': self.skill_id}))
        self.log.info('Done')

    def handle_idle(self, message):
        self.gui.show_page('idle.qml')

    def get_coming_days_forecast(self, forecast, unit, days=None):
        """
            Get weather forcast for the coming days and returns them as a list

            Parameters:
                forecast: OWM weather
                unit: Temperature unit
                dt: Reference time
                days: number of days to get forecast for, defaults to 4

            Returns: List of dicts containg weather info
        """
        days = days or 4
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        forecast_list = []
        # Get tomorrow and 4 days forward
        for weather in list(forecast.get_weathers())[1:5]:
            result_temp = weather.get_temperature(unit)
            day_num = datetime.weekday(
                datetime.fromtimestamp(weather.get_reference_time()))
            result_temp_day = weekdays[day_num]
            forecast_list.append({
                "weathercode": self.CODES[weather.get_weather_icon_name()],
                 "max": round(result_temp['max']),
                 "min": round(result_temp['min']),
                 "date": result_temp_day
            })
        return forecast_list

    def mark2_forecast(self, report):
        """ Builds forecast for the upcoming days for the Mark-2 display."""
        future_weather = self.owm.daily_forecast(report['full_location'],
                                                 report['lat'],
                                                 report['lon'], limit=5)
        f = future_weather.get_forecast()
        forecast_list = self.get_coming_days_forecast(f,
            self.__get_temperature_unit())

        if "gui" in dir(self):
            forecast = {}
            forecast['first'] = forecast_list[0:2]
            forecast['second'] = forecast_list[2:4]
            self.gui['forecast'] = forecast


    @intent_handler(IntentBuilder("").require("Query").one_of(
        "Weather", "Forecast").require("Weekend").require(
        "Next").optionally("Location").build())
    def handle_next_weekend_weather(self, message):
        """ Handle next weekends weather """
        try:
            report = self.__initialize_report(message)
            when, _ = extract_datetime('next saturday', lang='en-us')
            self.report_forecast(report, when)
            when, _ = extract_datetime('next sunday', lang='en-us')
            self.report_forecast(report, when)
        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    @intent_handler(IntentBuilder("").require("Query").one_of("Weather",
        "Forecast").require("Weekend").optionally("Location").build())
    def handle_weekend_weather(self, message):
        """ Handle weather for weekend. """
        try:
            report = self.__initialize_report(message)

            # Get a date from spoken request
            when, _ = extract_datetime('this saturday', lang='en-us')
            self.report_forecast(report, when)
            when, _ = extract_datetime('this sunday', lang='en-us')
            self.report_forecast(report, when)
        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    # Handle: what is the weather like?
    @intent_handler(IntentBuilder("").require("Query").require(
        "Weather").optionally("Location").build())
    def handle_current_weather(self, message):
        try:
            # Get a date from requests like "weather for next Tuesday"
            today = extract_datetime(" ")[0]
            when, _ = extract_datetime(
                        message.data.get('utterance'), lang=self.lang)
            if today != when:
                LOG.info("Doing a forecast" + str(today) + " " + str(when))
                return self.handle_forecast(message)

            report = self.__initialize_report(message)
            # Get current conditions
            currentWeather = self.owm.weather_at_place(
                report['full_location'], report['lat'],
                report['lon']).get_weather()

            # Change encoding of the localized report to utf8 if needed
            condition = currentWeather.get_detailed_status()
            if self.owm.encoding != 'utf8':
                condition = self.__translate(
                    condition.encode(self.owm.encoding).decode('utf8')
                )

            report['condition'] = condition
            report['temp'] = self.__get_temperature(currentWeather, 'temp')
            report['icon'] = currentWeather.get_weather_icon_name()

            # Get forecast for the day
            # can get 'min', 'max', 'eve', 'morn', 'night', 'day'
            # Set time to 12 instead of 00 to accomodate for timezones
            forecastWeather = self.__get_forecast(
                today.replace(
                    hour=12),
                report['full_location'],
                report['lat'],
                report['lon'])
            report['temp_min'] = self.__get_temperature(forecastWeather, 'min')
            report['temp_max'] = self.__get_temperature(forecastWeather, 'max')
            report['humidity'] = forecastWeather.get_humidity()

            wind = self.get_wind_speed(forecastWeather)
            report['wind'] = "{} {}".format(wind[0], wind[1] or "")

            self.__report_weather("current", report,
                separate_min_max='Location' not in message.data)
            self.mark2_forecast(report)
        except HTTPError as e:
            self.log.exception(repr(e))
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    # Handle: What is the weather forecast?
    @intent_handler(IntentBuilder("").require(
        "Forecast").optionally("Location").build())
    def handle_forecast(self, message):
        try:
            report = self.__initialize_report(message)

            # Get a date from spoken request
            when = extract_datetime(message.data.get('utterance'),
                                    lang=self.lang)[0]
            self.report_forecast(report, when)
        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    def __get_requested_unit(self, message):
        """ Get selected unit from message.

        Arguments:
            message (Message): messagebus message from intent service

        Returns:
            'fahrenheit', 'celsius' or None
        """
        if 'Unit' in message.data:
            if self.voc_match(message.data['Unit'], 'Fahrenheit'):
                return 'fahrenheit'
            else:
                return 'celsius'
        else:
            return None

    @intent_handler(IntentBuilder("").require("Query").require(
        "Temperature").optionally("Location").optionally("Unit").build())
    def handle_current_temperature(self, message):
        return self.__handle_typed(message, 'temperature')

    @intent_handler(IntentBuilder("").require("Query").require("High") \
        .optionally("Temperature").optionally("Location") \
        .optionally("Unit").build())
    def handle_high_temperature(self, message):
        return self.__handle_typed(message, 'high.temperature')

    @intent_handler(IntentBuilder("").require("Query").require("Low") \
        .optionally("Temperature").optionally("Location") \
        .optionally("Unit").build())
    def handle_low_temperature(self, message):
        return self.__handle_typed(message, 'low.temperature')

    @intent_handler(IntentBuilder("").require("ConfirmQuery").require(
        "Windy").optionally("Location").build())
    def handle_isit_windy(self, message):
        """ Handler for utterances similar to "is it windy today?" """
        report = self.__populate_report(message)
        dialog = []
        if 'day' in report:
            dialog.append('forecast')

        if int(report['wind']) >= 9:
            dialog.append('hard')
        elif int(report['wind']) >= 5:
            dialog.append('medium')
        else:
            dialog.append('light')
        dialog.append('wind')
        dialog = '.'.join(dialog)
        self.speak_dialog(dialog)

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Hot", "Cold").optionally("Location").build())
    def handle_isit_hot(self, message):
        """ Handler for utterances similar to
        is it hot today?, is it cold? will it be hot tomorrow?, etc
        """
        return self.__handle_typed(message, 'hot')

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Snowing").optionally("Location").build())
    def handle_isit_snowing(self, message):
        """ Handler for utterances similar to "is it snowing today?"
        """
        report = self.__populate_report(message)
        if self.voc_match(report['condition'], 'Snowing'):
            dialog = 'affirmative.condition'
        elif self.voc_match(report['condition'], 'SnowAlternatives'):
            dialog = 'snowing.alternative'
        else:
            dialog = 'no.snow.predicted'

        if report.get('day'):
            dialog = 'forecast.' + dialog
        self.speak_dialog(dialog, report)

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Clear").optionally("Location").build())
    def handle_isit_clear(self, message):
        """ Handler for utterances similar to "is it clear skies today?"
        """
        report = self.__populate_report(message)
        if self.voc_match(report['condition'], 'Clear'):
            dialog = 'affirmative.condition'
        elif self.voc_match(report['condition'], 'ClearAlternatives'):
            dialog = 'clear.alternative'
        else:
            dialog = 'no.clear.predicted'

        if report.get('day'):
            dialog = 'forecast.' + dialog
        self.speak_dialog(dialog, report)

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Cloudy").optionally("Location").build())
    def handle_isit_cloudy(self, message):
        """ Handler for utterances similar to "is it clear skies today?"
        """
        report = self.__populate_report(message)
        if self.voc_match(report['condition'], 'Cloudy'):
            dialog = 'affirmative.condition'
        elif self.voc_match(report['condition'], 'CloudyAlternatives'):
            dialog = 'cloudy.alternative'
        else:
            dialog = 'no.cloudy.predicted'

        if report.get('day'):
            dialog = 'forecast.' + dialog
        self.speak_dialog(dialog, report)

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Foggy").optionally("Location").build())
    def handle_isit_foggy(self, message):
        """ Handler for utterances similar to "is it foggy today?"
        """
        report = self.__populate_report(message)
        if self.voc_match(report['condition'], 'Foggy'):
            dialog = 'affirmative.condition'
        elif self.voc_match(report['condition'], 'FoggyAlternatives'):
            dialog = 'fog.alternative'
        else:
            dialog = 'no.fog.predicted'

        if report.get('day'):
            dialog = 'forecast.' + dialog
        self.speak_dialog(dialog, report)

    @intent_handler(IntentBuilder("").require("ConfirmQuery").one_of(
        "Raining").optionally("Location").build())
    def handle_isit_raining(self, message):
        """ Handler for utterances similar to "is it snowing today?"
        """
        report = self.__populate_report(message)
        if self.voc_match(report['condition'], 'Raining'):
            dialog  = 'affirmative.condition'
        elif self.voc_match(report['condition'], 'RainAlternatives'):
            dialog = 'raining.alternative'
        else:
            dialog = 'no.rain.predicted'

        if report.get('day'):
            dialog = 'forecast.' + dialog
        self.speak_dialog(dialog, report)

    def __handle_typed(self, message, response_type):
        try:
            unit = self.__get_requested_unit(message)
            # Get a date from requests like "weather for next Tuesday"
            today = extract_datetime(" ")[0]
            when, _ = extract_datetime(
                        message.data.get('utterance'), lang=self.lang)

            report = self.__initialize_report(message)
            if today != when:
                LOG.info("Doing a forecast" + str(today) + " " + str(when))
                return self.report_forecast(report, when,
                                            dialog=response_type)

            # Get current conditions
            currentWeather = self.owm.weather_at_place(
                report['full_location'], report['lat'],
                report['lon']).get_weather()

            # Change encoding of the localized report to utf8 if needed
            condition = currentWeather.get_detailed_status()
            if self.owm.encoding != 'utf8':
                condition = self.__translate(
                    condition.encode(self.owm.encoding).decode('utf8')
                )

            report['condition'] = condition
            report['temp'] = self.__get_temperature(currentWeather, 'temp',
                                                    unit)
            report['icon'] = currentWeather.get_weather_icon_name()

            # Get forecast for the day
            # can get 'min', 'max', 'eve', 'morn', 'night', 'day'
            # Set time to 12 instead of 00 to accomodate for timezones
            forecastWeather = self.__get_forecast(
                today.replace(
                    hour=12),
                report['full_location'],
                report['lat'],
                report['lon'])
            report['temp_min'] = self.__get_temperature(forecastWeather, 'min',
                                                        unit)
            report['temp_max'] = self.__get_temperature(forecastWeather, 'max',
                                                        unit)
            report['humidity'] = forecastWeather.get_humidity()

            wind = self.get_wind_speed(forecastWeather)
            report['wind'] = "{} {}".format(wind[0], wind[1] or "")

            self.__report_weather('current', report, response_type)
            self.mark2_forecast(report)
        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

    def __populate_report(self, message):
        try:
            unit = self.__get_requested_unit(message)
            # Get a date from requests like "weather for next Tuesday"
            today = extract_datetime(" ")[0]
            when, _ = extract_datetime(
                        message.data.get('utterance'), lang=self.lang)

            report = self.__initialize_report(message)
            if today != when:
                LOG.info("Doing a forecast" + str(today) + " " + str(when))
                return self.__populate_forecast(report, when)

            # Get current conditions
            currentWeather = self.owm.weather_at_place(
                report['full_location'], report['lat'],
                report['lon']).get_weather()

            # Change encoding of the localized report to utf8 if needed
            condition = currentWeather.get_detailed_status()
            if self.owm.encoding != 'utf8':
                condition = self.__translate(
                    condition.encode(self.owm.encoding).decode('utf8')
                )

            report['condition'] = condition
            report['temp'] = self.__get_temperature(currentWeather, 'temp',
                                                    unit)
            report['icon'] = currentWeather.get_weather_icon_name()

            # Get forecast for the day
            # can get 'min', 'max', 'eve', 'morn', 'night', 'day'
            # Set time to 12 instead of 00 to accomodate for timezones
            forecastWeather = self.__get_forecast(
                today.replace(
                    hour=12),
                report['full_location'],
                report['lat'],
                report['lon'])
            report['temp_min'] = self.__get_temperature(forecastWeather, 'min',
                                                        unit)
            report['temp_max'] = self.__get_temperature(forecastWeather, 'max',
                                                        unit)
            report['humidity'] = forecastWeather.get_humidity()

            wind = self.get_wind_speed(forecastWeather)
            report['wind'] = "{} {}".format(wind[0], wind[1] or "")
            return report

        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.exception("Error: {0}".format(e))

        return None

    def __populate_forecast(self, report, when, unit=None):
        """ Populate the report and return it.

        Arguments:
            report (dict): report base
            when : date for report
            unit: Unit type to use when presenting

        Returns: None if no report available otherwise dict with weather info
        """
        forecast_weather = self.__get_forecast(
            when, report['full_location'], report['lat'], report['lon'])
        if forecast_weather is None:
            return None # No forecast available

        # Can get temps for 'min', 'max', 'eve', 'morn', 'night', 'day'
        report['temp'] = self.__get_temperature(forecast_weather, 'day', unit)
        report['temp_min'] = self.__get_temperature(forecast_weather, 'min',
                                                    unit)
        report['temp_max'] = self.__get_temperature(forecast_weather, 'max',
                                                    unit)
        report['icon'] = forecast_weather.get_weather_icon_name()
        report['humidity'] = forecast_weather.get_humidity()
        report['wind'] = self.get_wind_speed(forecast_weather)[0]

        # TODO: Run off of status IDs instead of the status text?
        # This converts a status like "sky is clear" to a different
        # text and tense, because you don't want:
        # "Friday it will be 82 and the sky is clear", it should be
        # 'Friday it will be 82 and the sky will be clear' or just
        # 'Friday it will be 82 and clear.
        report['condition'] = self.__translate(
            forecast_weather.get_detailed_status(), True)

        report['day'] = self.__to_day(when)  # Tuesday, tomorrow, etc.
        return report

    def report_forecast(self, report, when, dialog='weather', unit=None):
        """ Speak forecast for specific day.

        Arguments:
            report (dict): report base
            when : date for report
            dialog (str): dialog type, defaults to 'weather'
            unit: Unit type to use when presenting
        """
        report = self.__populate_forecast(report, when, unit)
        if report is None:
            self.speak_dialog("no forecast", {'day': self.__to_day(when)})
            return

        self.__report_weather('forecast', report, rtype=dialog)

    # Handle: When will it rain again? | Will it rain on Tuesday?
    @intent_handler(IntentBuilder("").require("Query").require(
        "Next").require("Precipitation").optionally("Location").build())
    def handle_next_precipitation(self, message):
        report = self.__initialize_report(message)

        # Get a date from spoken request
        today = extract_datetime(" ")[0]
        when = extract_datetime(message.data.get('utterance'),
                                lang=self.lang)[0]

        # search the forecast for precipitation
        for weather in self.owm.daily_forecast(
                report['full_location'],
                report['lat'],
                report['lon'], 10).get_forecast().get_weathers():

            forecastDate = datetime.fromtimestamp(weather.get_reference_time())

            if when != today:
                # User asked about a specific date, is this it?
                whenGMT = self.__to_UTC(when)
                if forecastDate.date() != whenGMT.date():
                    continue

            rain = weather.get_rain()
            if rain and rain["all"] > 0:
                data = {
                    "modifier": "",
                    "precip": "rain",
                    "day": self.__to_day(forecastDate)
                }
                if rain["all"] < 10:
                    data["modifier"] = self.__translate("light")
                elif rain["all"] > 20:
                    data["modifier"] = self.__translate("heavy")

                self.speak_dialog("precipitation expected", data)
                return

            snow = weather.get_snow()
            if snow and snow["all"] > 0:
                data = {
                    "modifier": "",
                    "precip": "snow",
                    "day": self.__to_day(forecastDate)
                }
                if snow["all"] < 10:
                    data["modifier"] = self.__translate("light")
                elif snow["all"] > 20:
                    data["modifier"] = self.__translate("heavy")

                self.speak_dialog("precipitation expected", data)
                return

        self.speak_dialog("no precipitation expected", report)

    # Handle: What's the weather later?
    @intent_handler(IntentBuilder("").require("Query").require(
        "Weather").optionally("Location").require("Later").build())
    def handle_next_hour(self, message):
        try:
            report = self.__initialize_report(message)

            # Get near-future forecast
            forecastWeather = self.owm.three_hours_forecast(
                report['full_location'],
                report['lat'],
                report['lon']).get_forecast().get_weathers()[0]

            # NOTE: The 3-hour forecast uses different temperature labels,
            # temp, temp_min and temp_max.
            report['temp'] = self.__get_temperature(forecastWeather, 'temp')
            report['temp_min'] = self.__get_temperature(forecastWeather,
                                                        'temp_min')
            report['temp_max'] = self.__get_temperature(forecastWeather,
                                                        'temp_max')
            report['condition'] = forecastWeather.get_detailed_status()
            report['icon'] = forecastWeather.get_weather_icon_name()

            self.__report_weather("hour", report)
        except HTTPError as e:
            self.__api_error(e)
        except Exception as e:
            LOG.error("Error: {0}".format(e))

    # Handle: How humid is it?
    @intent_handler(IntentBuilder("").require(
        "Query").optionally("Location").require("Humidity").build())
    def handle_humidity(self, message):
        report = self.__initialize_report(message)

        when = extract_datetime(message.data.get('utterance'),
                                lang=self.lang)[0]
        if when == extract_datetime(" ")[0]:
            weather = self.owm.weather_at_place(
                report['full_location'],
                report['lat'],
                report['lon']).get_weather()
        else:
            # Get forecast for that day
            weather = self.__get_forecast(
                when, report['full_location'], report['lat'], report['lon'])
        if not weather or weather.get_humidity() == 0:
            self.speak_dialog("do not know")
            return

        value = str(weather.get_humidity()) + "%"
        self.__report_condition(self.__translate("humidity"), value, when)

    # Handle: How windy is it?
    @intent_handler(IntentBuilder("").require(
        "Query").optionally("Location").require("Windy").build())
    def handle_windy(self, message):
        report = self.__initialize_report(message)

        when = extract_datetime(message.data.get('utterance'))[0]
        if when == extract_datetime(" ")[0]:
            weather = self.owm.weather_at_place(
                report['full_location'],
                report['lat'],
                report['lon']).get_weather()
        else:
            # Get forecast for that day
            weather = self.__get_forecast(
                when, report['full_location'], report['lat'], report['lon'])
        if not weather or weather.get_wind() == 0:
            self.speak_dialog("do not know")
            return

        speed, dir, unit = self.get_wind_speed(weather)
        if dir:
            dir = self.__translate(dir)
            value = self.__translate("wind.speed.dir",
                                     data={"dir": dir,
                                           "speed": nice_number(speed),
                                           "unit": unit})
        else:
            value = self.__translate("wind.speed",
                                     data={"speed": nice_number(speed),
                                           "unit": unit})

        self.__report_condition(self.__translate("winds"), value, when)

    def get_wind_speed(self, weather):
        wind = weather.get_wind()

        speed = wind["speed"]
        # get speed
        if self.__get_speed_unit() == "mph":
            speed *= 2.23694
            unit = self.__translate("miles per hour")
        else:
            unit = self.__translate("meters per second")
        speed = round(speed)

        # get direction, convert compass degrees to named direction
        if "deg" in wind:
            deg = wind["deg"]
            if deg < 22.5:
                dir = "N"
            elif deg < 67.5:
                dir = "NE"
            elif deg < 112.5:
                dir = "E"
            elif deg < 157.5:
                dir = "SE"
            elif deg < 202.5:
                dir = "S"
            elif deg < 247.5:
                dir = "SW"
            elif deg < 292.5:
                dir = "W"
            elif deg < 337.5:
                dir = "NW"
            else:
                dir = "N"
        else:
            dir = None

        return speed, dir, unit

    # Handle: When is the sunrise?
    @intent_handler(IntentBuilder("").require(
        "Query").optionally("Location").require("Sunrise").build())
    def handle_sunrise(self, message):
        report = self.__initialize_report(message)

        when = extract_datetime(message.data.get('utterance'))[0]
        if when == extract_datetime(" ")[0]:
            weather = self.owm.weather_at_place(
                report['full_location'],
                report['lat'],
                report['lon']).get_weather()
        else:
            # Get forecast for that day
            # weather = self.__get_forecast(when, report['full_location'],
            #                               report['lat'], report['lon'])

            # There appears to be a bug in OWM, it can't extract the sunrise/
            # sunset from forecast objects.  Look in to this later, but say
            # "I don't know" for now
            weather = None
        if not weather or weather.get_humidity() == 0:
            self.speak_dialog("do not know")
            return

        dtSunriseUTC = datetime.fromtimestamp(weather.get_sunrise_time())
        dtLocal = self.__to_Local(dtSunriseUTC)
        self.speak(self.__nice_time(dtLocal, lang=self.lang, use_ampm=True))

    # Handle: When is the sunset?
    @intent_handler(IntentBuilder("").require(
        "Query").optionally("Location").require("Sunset").build())
    def handle_sunset(self, message):
        report = self.__initialize_report(message)

        when = extract_datetime(message.data.get('utterance'))[0]
        if when == extract_datetime(" ")[0]:
            weather = self.owm.weather_at_place(
                report['full_location'],
                report['lat'],
                report['lon']).get_weather()
        else:
            # Get forecast for that day
            # weather = self.__get_forecast(when, report['full_location'],
            #                               report['lat'], report['lon'])

            # There appears to be a bug in OWM, it can't extract the sunrise/
            # sunset from forecast objects.  Look in to this later, but say
            # "I don't know" for now
            weather = None
        if not weather or weather.get_humidity() == 0:
            self.speak_dialog("do not know")
            return

        dtSunriseUTC = datetime.fromtimestamp(weather.get_sunset_time())
        dtLocal = self.__to_Local(dtSunriseUTC)
        self.speak(self.__nice_time(dtLocal, lang=self.lang, use_ampm=True))

    def __get_location(self, message):
        """ Attempt to extract a location from the spoken phrase.

        If none is found return the default location instead.

        Arguments:
            message (Message): messagebus message
        Returns: tuple (lat, long, location string)
        """
        try:
            location = message.data.get("Location", None) if message else None
            if location:
                return None, None, location, location

            location = self.location

            if isinstance(location, dict):
                lat = location["coordinate"]["latitude"]
                lon = location["coordinate"]["longitude"]
                city = location["city"]
                state = city["state"]
                return lat, lon, city["name"] + ", " + state["name"] + \
                    ", " + state["country"]["name"], self.location_pretty

            return None
        except BaseException:
            self.speak_dialog("location.not.found")
            raise ValueError("Location not found")

    def __initialize_report(self, message):
        """ Creates a report base with location, unit. """
        lat, lon, location, pretty_location = self.__get_location(message)
        temp_unit = self.__get_requested_unit(message)
        return {
            'lat': lat,
            'lon': lon,
            'location': pretty_location,
            'full_location': location,
            'scale': self.translate(temp_unit or self.__get_temperature_unit())
        }

    def __report_weather(self, timeframe, report, rtype='weather',
                         separate_min_max=False):
        """ Report the weather verbally and visually.

        Produces an utterance based on the timeframe and rtype parameters.
        The report also provides location context. The dialog file used will
        be:
            "timeframe(.local).rtype"

        Arguments:
            timeframe (str): 'current' or 'future'.
            report (dict): Dictionary with report information (temperatures
                           and such.
            rtype (str): report type, defaults to 'weather'
            separate_min_max (bool): a separate dialog for min max temperatures
                                     will be output if True (default: False)
        """

        # Convert code to matching weather icon on Mark 1
        if report['location']:
            report['location'] = self.owm.location_translations.get(report['location'], report['location'])
        weather_code = str(report['icon'])
        img_code = self.CODES[weather_code]

        # Display info on a screen
        # Mark-2
        self.gui["current"] = report["temp"]
        self.gui["min"] = report["temp_min"]
        self.gui["max"] = report["temp_max"]
        self.gui["location"] = report["full_location"].replace(', ', '\n')
        self.gui["condition"] = report["condition"]
        self.gui["icon"] = report["icon"]
        self.gui["weathercode"] = img_code
        self.gui["humidity"] = report.get("humidity", "--")
        self.gui["wind"] = report.get("wind", "--")
        self.gui.show_pages(["weather.qml", "highlow.qml",
                             "forecast1.qml", "forecast2.qml"])
        # Mark-1
        self.enclosure.deactivate_mouth_events()
        self.enclosure.weather_display(img_code, report['temp'])

        dialog_name = timeframe
        if report['location'] == self.location_pretty:
            dialog_name += ".local"
        self.speak_dialog(dialog_name + "." + rtype, report)

        # Just show the icons while still speaking
        mycroft.audio.wait_while_speaking()

        # Speak the high and low temperatures
        if separate_min_max:
            self.speak_dialog('min.max', report)
            self.gui.show_page("highlow.qml")
            mycroft.audio.wait_while_speaking()

        self.enclosure.activate_mouth_events()
        self.enclosure.mouth_reset()

    def __report_condition(self, name, value, when):
        # Report a specific value
        data = {
            "condition": name,
            "value": value,
        }
        if when == extract_datetime(" ")[0]:
            self.speak_dialog("report.condition", data)
        else:
            data["day"] = self.__to_day(when)
            self.speak_dialog("report.future.condition", data)

    def __get_forecast(self, when, location, lat, lon):
        """ Get a forecast for the given time and location.

        Arguments:
            when (datetime): Local datetime for report
            location: location
            lat: Latitude for report
            lon: Longitude for report
        """

        # convert time to UTC/GMT (forecast is in GMT)
        whenGMT = self.__to_UTC(when)

        # search for the requested date in the returned forecast data
        forecasts = self.owm.daily_forecast(location, lat, lon, limit=10).get_forecast()
        for weather in forecasts.get_weathers():
            forecastDate = datetime.fromtimestamp(weather.get_reference_time())
            if forecastDate.date() == whenGMT.date():
                # found the right day, now format up the results
                return weather

        # No forecast for the given day
        return None

    def __get_speed_unit(self):
        """ Get speed unit based on config setting.

        Config setting of 'metric' will return "meters_sec", otherwise 'mph'

        Returns: (str) 'meters_sec' or 'mph'
        """
        system_unit = self.config_core.get('system_unit')
        return system_unit == "metric" and "meters_sec" or "mph"

    def __get_temperature_unit(self):
        """ Get temperature unit from config and skill settings.

        Config setting of 'metric' implies celsius for unit
        
        Returns: (str) "celcius" or "fahrenheit"
        """
        system_unit = self.config_core.get('system_unit')
        override = self.settings.get("units", "")
        if override:
            if override[0].lower() == "f":
                return "fahrenheit"
            elif override[0].lower() == "c":
                return "celsius"

        return system_unit == "metric" and "celsius" or "fahrenheit"

    def __get_temperature(self, weather, key, unit=None):
        # Extract one of the temperatures from the weather data.
        # Typically it has: 'temp', 'min', 'max', 'morn', 'day', 'night'
        try:
            unit = unit or self.__get_temperature_unit()
            return str(int(round(weather.get_temperature(unit)[key])))
        except BaseException:
            return ""

    def __api_error(self, e):
        if e.response.status_code == 401:
            from mycroft import Message
            self.bus.emit(Message("mycroft.not.paired"))

    def __to_day(self, when):
        # TODO: This will be a compatibility wrapper for
        #       mycroft.util.format.relative_day(when)
        if self.lang.lower().startswith("sv"):
            days = ['Måndag', 'Tisdag', 'Onsdag', 'Torsdag', 'Fredag',
                    'Lördag', 'Söndag']
        elif self.lang.lower().startswith("de"):
            days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag',
                    'Samstag', 'Sonntag']
        elif self.lang.lower().startswith("es"):
            days = ['Lunes', 'Martes', u'Miércoles',
                    'Jueves', 'Viernes', u'Sábado', 'Domingo']
        elif self.lang.lower().startswith("fr"):
            days = ["Lundi", "Mardi", "Mercredi",
                    "Jeudi", "Vendredi", "Samedi", "Dimanche"]
        elif self.lang.lower().startswith("it"):
            days = ['Lunedi', 'Martedi', 'Mercoledi',
                    'Giovedi', 'Venerdi', 'Sabato', 'Domenica']
        elif self.lang.lower().startswith("pt"):
            days = ['Segunda', 'Terca', 'Quarta',
                    'Quinta', 'Sexta', 'Sabado', 'Domingo']
        else:
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
        return days[when.weekday()]

    def __to_UTC(self, when):
        try:
            # First try with modern mycroft.util.time functions
            return to_utc(when)
        except Exception:
            # TODO: This uses the device timezone -- should probably use
            #       the timezone of the location being forecasted
            timezone = pytz.timezone(self.location["timezone"]["code"])
            return timezone.localize(when).astimezone(pytz.utc)

    def __to_Local(self, when):
        try:
            # First try with modern mycroft.util.time functions
            return to_local(when)
        except Exception:
            # Fallback to the old pytz code
            if not when.tzinfo:
                when = when.replace(tzinfo=pytz.utc)
            timezone = pytz.timezone(self.location["timezone"]["code"])
            return when.astimezone(timezone)

    def __translate(self, condition, future=False, data=None):
        # behaviour of method dialog_renderer.render(...) has changed - instead
        # of exception when given template is not found now simply the
        # templatename is returned!?!
        if future:
            if (condition + ".future") in self.dialog_renderer.templates:
                return self.dialog_renderer.render(condition + ".future", data)

        if condition in self.dialog_renderer.templates:
            return self.dialog_renderer.render(condition, data)
        else:
            return condition

    def __nice_time(self, dt, lang="en-us", speech=True, use_24hour=False,
                    use_ampm=False):
        # compatibility wrapper for nice_time
        nt_supported_languages = ['en','es','it','fr','de','hu','nl','da']
        if not (lang[0:2] in nt_supported_languages):
            lang = "en-us"
        return nice_time(dt, lang, speech, use_24hour, use_ampm)

def create_skill():
    return WeatherSkill()
