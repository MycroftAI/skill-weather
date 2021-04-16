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
"""Representations and conversions of the data returned by the weather API."""
from datetime import time, timedelta

from mycroft.util.time import now_local
from .config import MILES_PER_HOUR
from .util import convert_to_local_datetime

THIRTY_PERCENT = 30
SATURDAY = 5
SUNDAY = 6
WIND_DIRECTION_CONVERSION = (
    (22.5, "north"),
    (67.5, "northeast"),
    (112.5, "east"),
    (157.5, "southeast"),
    (202.5, "south"),
    (247.5, "southwest"),
    (292.5, "west"),
    (337.5, "northwest"),
)


def is_daily_forecast(weather_report) -> bool:
    """Helper function to determine if the object passed is a DailyWeather object."""
    return isinstance(weather_report, DailyWeather)


def is_hourly_forecast(weather_report) -> bool:
    """Helper function to determine if the object passed is a HourlyWeather object."""
    return isinstance(weather_report, HourlyWeather)


def is_current_weather(weather_report) -> bool:
    """Helper function to determine if the object passed is a CurrentWeather object."""
    return isinstance(weather_report, CurrentWeather)


class WeatherCondition:
    """Data representation of a weather conditions JSON object from the API"""

    def __init__(self, conditions: dict):
        self.id = conditions["id"]
        self.category = conditions["main"]
        self.description = conditions["description"]
        self.icon = conditions["icon"]


class Weather:
    """Abstract data representation of commonalities in forecast types."""

    def __init__(self, weather: dict, timezone: str):
        self.date_time = convert_to_local_datetime(weather["dt"], timezone)
        self.feels_like = weather["feelsLike"]
        self.pressure = weather["pressure"]
        self.humidity = weather["humidity"]
        self.dew_point = weather["dewPoint"]
        self.clouds = weather["clouds"]
        self.wind_speed = int(weather["windSpeed"])
        self.wind_direction = self._determine_wind_direction(weather["windDeg"])
        self.condition = WeatherCondition(weather["weather"][0])

    @staticmethod
    def _determine_wind_direction(degree_direction: int):
        """Convert wind direction from compass degrees to compass direction.

        :param degree_direction: Degrees on a compass indicating wind direction.
        """
        wind_direction = None
        for min_degree, compass_direction in WIND_DIRECTION_CONVERSION:
            if degree_direction < min_degree:
                wind_direction = compass_direction
                break
        if wind_direction is None:
            wind_direction = "north"

        return wind_direction

    def determine_wind_strength(self, speed_unit: str):
        """Convert a wind speed to a wind strength.

        :param speed_unit: unit of measure for speed depending on device configuration
        """
        if speed_unit == MILES_PER_HOUR:
            limits = dict(strong=20, moderate=11)
        else:
            limits = dict(strong=9, moderate=5)
        if self.wind_speed >= limits["strong"]:
            wind_strength = "strong"
        elif self.wind_speed >= limits["moderate"]:
            wind_strength = "moderate"
        else:
            wind_strength = "light"

        return wind_strength


class CurrentWeather(Weather):
    """Data representation of the current weather returned by the API"""

    def __init__(self, weather: dict, timezone: str):
        super().__init__(weather, timezone)
        self.sunrise = convert_to_local_datetime(weather["sunrise"], timezone)
        self.sunset = convert_to_local_datetime(weather["sunset"], timezone)
        self.temperature = round(weather["temp"])
        self.visibility = weather["visibility"]
        self.low_temperature = None
        self.high_temperature = None


class DailyFeelsLike:
    """Data representation of a "feels like" JSON object from the API"""

    def __init__(self, temperatures: dict):
        self.day = round(temperatures["day"])
        self.night = round(temperatures["night"])
        self.evening = round(temperatures["eve"])
        self.morning = round(temperatures["morn"])


class DailyTemperature(DailyFeelsLike):
    """Data representation of a temperatures JSON object from the API"""

    def __init__(self, temperatures: dict):
        super().__init__(temperatures)
        self.low = round(temperatures["min"])
        self.high = round(temperatures["max"])


class DailyWeather(Weather):
    """Data representation of a daily forecast JSON object from the API"""

    def __init__(self, weather: dict, timezone: str):
        super().__init__(weather, timezone)
        self.sunrise = convert_to_local_datetime(weather["sunrise"], timezone)
        self.sunset = convert_to_local_datetime(weather["sunset"], timezone)
        self.temperature = DailyTemperature(weather["temp"])
        self.feels_like = DailyFeelsLike(weather["feelsLike"])
        self.chance_of_precipitation = int(weather["pop"] * 100)


class HourlyWeather(Weather):
    """Data representation of a hourly forecast JSON object from the API"""

    def __init__(self, weather: dict, timezone: str):
        super().__init__(weather, timezone)
        self.temperature = round(weather["temp"])
        self.chance_of_precipitation = int(weather["pop"] * 100)


class WeatherAlert:
    """Data representation of a weather conditions JSON object from the API"""

    def __init__(self, alert: dict, timezone: str):
        self.sender = alert.get("sender_name")
        self.event = alert["event"]
        self.start = convert_to_local_datetime(alert["start"], timezone)
        self.end = convert_to_local_datetime(alert["end"], timezone)
        self.description = alert["description"]


class WeatherReport:
    """Full representation of the data returned by the Open Weather Maps One Call API"""

    def __init__(self, report):
        timezone = report["timezone"]
        self.current = CurrentWeather(report["current"], timezone)
        self.hourly = [HourlyWeather(hour, timezone) for hour in report["hourly"]]
        self.daily = [DailyWeather(day, timezone) for day in report["daily"]]
        today = self.daily[0]
        self.current.high_temperature = today.temperature.high
        self.current.low_temperature = today.temperature.low
        if "alerts" in report:
            self.alerts = [WeatherAlert(alert, timezone) for alert in report["alerts"]]
        else:
            self.alerts = None

    def get_weather_for_intent(self, intent_data):
        """Use the intent to determine which forecast satisfies the request"""
        if intent_data.timeframe == "hourly":
            weather = self.get_forecast_for_hour(intent_data)
        elif intent_data.timeframe == "daily":
            weather = self.get_forecast_for_date(intent_data)
        else:
            weather = self.current

        return weather

    def get_forecast_for_date(self, intent_data):
        """Use the intent to determine which daily forecast(s) satisfies the request"""
        if intent_data.intent_datetime.date() == intent_data.location_datetime.date():
            forecast = self.daily[0]
        else:
            delta = intent_data.intent_datetime - intent_data.location_datetime
            day_delta = int(delta / timedelta(days=1))
            day_index = day_delta + 1
            forecast = self.daily[day_index]

        return forecast

    def get_forecast_for_multiple_days(self, days):
        """Use the intent to determine which daily forecast(s) satisfies the request"""
        if days > 7:
            raise IndexError("Only seven days of forecasted weather available.")

        forecast = self.daily[1 : days + 1]

        return forecast

    def get_forecast_for_hour(self, intent_data):
        """Use the intent to determine which hourly forecast(s) satisfies the request"""
        delta = intent_data.intent_datetime - intent_data.location_datetime
        hour_delta = int(delta / timedelta(hours=1))
        hour_index = hour_delta + 1
        report = self.hourly[hour_index]

        return report

    def get_weekend_forecast(self):
        """Use the intent to determine which daily forecast(s) satisfies the request"""
        forecast = list()
        for forecast_day in self.daily:
            report_date = forecast_day.date_time.date()
            if report_date.weekday() in (SATURDAY, SUNDAY):
                forecast.append(forecast_day)

        return forecast

    def get_next_precipitation(self, intent_data):
        """Determine when the next chance of precipitation is in the forecast"""
        report = None
        current_precipitation = True
        timeframe = "hourly"
        for hourly in self.hourly:
            if hourly.date_time.date() > intent_data.location_datetime.date():
                break
            if hourly.chance_of_precipitation > THIRTY_PERCENT:
                if not current_precipitation:
                    report = hourly
                    break
            else:
                current_precipitation = False

        if report is None:
            timeframe = "daily"
            for daily in self.daily:
                if daily.date_time.date() == intent_data.location_datetime.date():
                    continue
                if daily.chance_of_precipitation > THIRTY_PERCENT:
                    report = daily
                    break

        return report, timeframe
