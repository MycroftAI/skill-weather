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
