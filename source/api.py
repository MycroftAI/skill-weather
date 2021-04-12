# Copyright 2021, Mycroft AI Inc.
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
from requests import HTTPError

from mycroft.api import Api
from .weather import WeatherReport
from .util import LocationNotFoundError

MINUTES = 60  # Minutes to seconds multiplier

APIErrors = (LocationNotFoundError, HTTPError)


class OpenWeatherMapApi(Api):
    def __init__(self):
        super().__init__(path="owm")

    def get_weather_for_coordinates(self, measurement_system, latitude, longitude):
        """Use the One Call API to get local weather conditions."""
        query_parameters = dict(
            exclude="minutely",
            lat=latitude,
            lon=longitude,
            units=measurement_system
        )
        api_request = dict(path="/onecall", query=query_parameters)
        response = self.request(api_request)
        local_weather = WeatherReport(response)

        return local_weather
