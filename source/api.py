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
"""Call the Open Weather Map One Call API through Selene.

The One Call API provides current weather, 48 hourly forecasts, 7 daily forecasts
and weather alert data all in a single API call.  The endpoint is passed a
latitude and longitude from either the user's configuration or a requested
location.

It also supports returning values in the measurement system (Metric/Imperial)
provided, precluding us from having to do the conversions.

"""
from mycroft.api import Api
from .weather import WeatherReport


class OpenWeatherMapApi(Api):
    """Use Open Weather Map's One Call API to retrieve weather information"""

    def __init__(self):
        super().__init__(path="owm")

    def get_weather_for_coordinates(
        self, measurement_system: str, latitude: float, longitude: float
    ) -> WeatherReport:
        """Issue an API call and map the return value into a weather report

        :param measurement_system: Metric or Imperial measurement units
        :param latitude: the geologic latitude of the weather location
        :param longitude: the geologic longitude of the weather location
        """
        query_parameters = dict(
            exclude="minutely", lat=latitude, lon=longitude, units=measurement_system
        )
        api_request = dict(path="/onecall", query=query_parameters)
        response = self.request(api_request)
        local_weather = WeatherReport(response)

        return local_weather
