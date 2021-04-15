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
"""Mycroft skill for communicating weather information

This skill uses the Open Weather Map One Call API to retrieve weather data
from around the globe (https://openweathermap.org/api/one-call-api).  It
proxies its calls to the API through Mycroft's officially supported API,
Selene.  The Selene API is also used to get geographical information about the
city name provided in the request.
"""
from collections import defaultdict
from multi_key_dict import multi_key_dict
from time import sleep
from typing import List, Tuple

from adapt.intent import IntentBuilder
from requests import HTTPError

import mycroft.audio
from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus.message import Message
from mycroft.util.parse import extract_number
from .source import (
    DailyWeather,
    LocationNotFoundError,
    OpenWeatherMapApi,
    WeatherConfig,
    WeatherDialog,
    WeatherIntent,
    WeatherReport,
)

# TODO: VK Failures
#   Locations: Washington, D.C.
#
# TODO: Intent failures
#   Later weather: only the word "later" in the vocab file works all others
#       invoke datetime skill

MARK_II = "mycroft_mark_2"
TWELVE_HOUR = "half"
CLEAR = 0
PARTLY_CLOUDY = 1
CLOUDY = 2
LIGHT_RAIN = 3
RAIN = 4
THUNDERSTORM = 5
SNOW = 6
WINDY = 7


class WeatherSkill(MycroftSkill):
    """Main skill code for the weather skill."""

    def __init__(self):
        super().__init__("WeatherSkill")
        self.weather_api = OpenWeatherMapApi()
        self.weather_config = WeatherConfig(self.config_core, self.settings)
        self.platform = self.config_core["enclosure"]["platform"]

        # Build a dictionary to translate OWM weather-conditions
        # codes into the Mycroft weather icon codes
        # (see https://openweathermap.org/weather-conditions)
        self.image_codes = multi_key_dict()
        self.image_codes["01d", "01n"] = CLEAR
        self.image_codes["02d", "02n", "03d", "03n"] = PARTLY_CLOUDY
        self.image_codes["04d", "04n"] = CLOUDY
        self.image_codes["09d", "09n"] = LIGHT_RAIN
        self.image_codes["10d", "10n"] = RAIN
        self.image_codes["11d", "11n"] = THUNDERSTORM
        self.image_codes["13d", "13n"] = SNOW
        self.image_codes["50d", "50n"] = WINDY

        # Use Mycroft proxy if no private key provided
        self.settings["api_key"] = None
        self.settings["use_proxy"] = True

    @intent_handler(
        IntentBuilder("")
        .one_of("Weather", "Forecast")
        .optionally("Query")
        .optionally("Location")
        .optionally("Today")
    )
    def handle_current_weather(self, message: Message):
        """Handle current weather requests such as: what is the weather like?

        :param message: Message Bus event information from the intent parser
        """
        self._report_current_weather(message)

    @intent_handler(
        IntentBuilder("")
        .require("Query")
        .require("Like")
        .require("Outside")
        .optionally("Location")
        .optionally("Today")
    )
    def handle_like_outside(self, message: Message):
        """Handle current weather requests such as: what's it like outside?

        :param message: Message Bus event information from the intent parser
        """
        self._report_current_weather(message)

    @intent_handler("what.is.multi.day.forecast.intent")
    def handle_multi_day_forecast(self, message: Message):
        """Handle multiple day forecast without specified location.

        Examples:
            "What is the 3 day forecast?"
            "What is the weather forecast?"

        :param message: Message Bus event information from the intent parser
        """
        if self.voc_match(message.data["num"], "Couple"):
            days = 2
        else:
            days = int(extract_number(message.data["num"]))
            if days > 7:
                self.speak_dialog("seven.days.available")
                days = 7
        self._report_multi_day_forecast(message, days)

    @intent_handler(
        IntentBuilder("")
        .one_of("Weather", "Forecast")
        .optionally("Query")
        .require("RelativeDay")
        .optionally("Location")
    )
    def handle_one_day_forecast(self, message):
        """Handle forecast for a single day.

        Examples:
            "What is the weather forecast tomorrow?"
            "What is the weather forecast on Tuesday in Baltimore?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_one_day_forecast(message)

    @intent_handler(
        IntentBuilder("")
        .require("Query")
        .require("Weather")
        .require("Later")
        .optionally("Location")
    )
    def handle_next_hour(self, message: Message):
        """Handle future weather requests such as: what's the weather later?

        :param message: Message Bus event information from the intent parser
        """
        self._report_one_hour_weather(message)

    @intent_handler(
        IntentBuilder("")
        .require("RelativeTime")
        .one_of("Weather", "Forecast")
        .optionally("Query")
        .optionally("RelativeDay")
        .optionally("Location")
    )
    def handle_weather_at_time(self, message: Message):
        """Handle future weather requests such as: what's the weather tonight?

        :param message: Message Bus event information from the intent parser
        """
        self._report_one_hour_weather(message)

    @intent_handler(
        IntentBuilder("")
        .require("Query")
        .one_of("Weather", "Forecast")
        .require("Weekend")
        .optionally("Location")
    )
    def handle_weekend_forecast(self, message: Message):
        """Handle requests for the weekend forecast.

        :param message: Message Bus event information from the intent parser
        """
        self._report_weekend_forecast(message)

    @intent_handler(
        IntentBuilder("")
        .optionally("Query")
        .one_of("Weather", "Forecast")
        .require("Week")
        .optionally("Location")
    )
    def handle_week_weather(self, message: Message):
        """Handle weather for week (i.e. seven days).

        :param message: Message Bus event information from the intent parser
        """
        self._report_multi_day_forecast(message, days=7)

    @intent_handler(
        IntentBuilder("")
        .require("Temperature")
        .optionally("Query")
        .optionally("Location")
        .optionally("Unit")
        .optionally("Today")
        .optionally("Now")
    )
    def handle_current_temperature(self, message: Message):
        """Handle requests for current temperature.

        Examples:
            "What is the temperature in Celsius?"
            "What is the temperature in Baltimore?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message, temperature_type="current")

    @intent_handler(
        IntentBuilder("")
        .optionally("Query")
        .require("Temperature")
        .optionally("Location")
        .optionally("Unit")
        .optionally("RelativeDay")
        .optionally("Now")
    )
    def handle_simple_temperature(self, message: Message):
        """Handle simple requests for current temperature.

        Examples: "What is the temperature?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message, temperature_type="current")

    @intent_handler(
        IntentBuilder("")
        .require("RelativeTime")
        .require("Temperature")
        .optionally("Query")
        .optionally("RelativeDay")
        .optionally("Location")
    )
    def handle_temperature_at_time(self, message: Message):
        """Handle requests for current temperature at a relative time.

        Examples:
            "What is the temperature tonight?"
            "What is the temperature tomorrow morning?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message)

    @intent_handler(
        IntentBuilder("")
        .optionally("Query")
        .require("High")
        .optionally("Temperature")
        .optionally("Location")
        .optionally("Unit")
        .optionally("RelativeDay")
    )
    def handle_high_temperature(self, message: Message):
        """Handle a request for the high temperature.

        Examples:
            "What is the high temperature tomorrow?"
            "What is the high temperature in London on Tuesday?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message, temperature_type="high")

    @intent_handler(
        IntentBuilder("")
        .optionally("Query")
        .require("Low")
        .optionally("Temperature")
        .optionally("Location")
        .optionally("Unit")
        .optionally("RelativeDay")
    )
    def handle_low_temperature(self, message: Message):
        """Handle a request for the high temperature.

        Examples:
            "What is the high temperature tomorrow?"
            "What is the high temperature in London on Tuesday?"

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message, temperature_type="low")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQueryCurrent")
        .one_of("Hot", "Cold")
        .optionally("Location")
        .optionally("Today")
    )
    def handle_is_it_hot(self, message: Message):
        """Handler for temperature requests such as: is it going to be hot today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_temperature(message, "current")

    @intent_handler(
        IntentBuilder("")
        .optionally("How")
        .one_of("Hot", "Cold")
        .one_of("ConfirmQueryFuture", "ConfirmQueryCurrent")
        .optionally("Location")
        .optionally("RelativeDay")
    )
    def handle_how_hot_or_cold(self, message):
        """Handler for temperature requests such as: how cold will it be today?

        :param message: Message Bus event information from the intent parser
        """
        temperature_type = "high" if message.data.get("Hot") else "low"
        self._report_temperature(message, temperature_type)

    @intent_handler(
        IntentBuilder("")
        .require("How")
        .one_of("Hot", "Cold")
        .one_of("ConfirmQueryFuture", "ConfirmQueryCurrent")
        .optionally("Location")
        .optionally("RelativeDay")
    )
    def handle_how_hot_or_cold_alt(self, message: Message):
        """Handler for temperature requests such as: how cold will it be today?

        :param message: Message Bus event information from the intent parser
        """
        temperature_type = "high" if message.data.get("Hot") else "low"
        self._report_temperature(message, temperature_type)

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Windy")
        .optionally("Location")
        .optionally("RelativeDay")
    )
    def handle_is_it_windy(self, message: Message):
        """Handler for weather requests such as: is it windy today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_wind(message)

    @intent_handler(
        IntentBuilder("")
        .require("How")
        .require("Windy")
        .optionally("Location")
        .optionally("ConfirmQuery")
        .optionally("RelativeDay")
    )
    def handle_windy(self, message):
        """Handler for weather requests such as: how windy is it?

        :param message: Message Bus event information from the intent parser
        """
        self._report_wind(message)

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Snowing")
        .optionally("Location")
    )
    def handle_is_it_snowing(self, message: Message):
        """Handler for weather requests such as: is it snowing today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Snow")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Clear")
        .optionally("Location")
    )
    def handle_is_it_clear(self, message: Message):
        """Handler for weather requests such as: is the sky clear today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, condition="Clear")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Cloudy")
        .optionally("Location")
        .optionally("RelativeTime")
    )
    def handle_is_it_cloudy(self, message: Message):
        """Handler for weather requests such as: is it cloudy today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Clouds")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Foggy")
        .optionally("Location")
    )
    def handle_is_it_foggy(self, message: Message):
        """Handler for weather requests such as: is it foggy today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Fog")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Raining")
        .optionally("Location")
    )
    def handle_is_it_raining(self, message: Message):
        """Handler for weather requests such as: is it raining today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Rain")

    @intent_handler("do.i.need.an.umbrella.intent")
    def handle_need_umbrella(self, message: Message):
        """Handler for weather requests such as: will I need an umbrella today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Rain")

    @intent_handler(
        IntentBuilder("")
        .require("ConfirmQuery")
        .require("Storm")
        .optionally("Location")
    )
    def handle_is_it_storming(self, message: Message):
        """Handler for weather requests such as:  is it storming today?

        :param message: Message Bus event information from the intent parser
        """
        self._report_weather_condition(message, "Thunderstorm")

    @intent_handler(
        IntentBuilder("")
        .require("When")
        .optionally("Next")
        .require("Precipitation")
        .optionally("Location")
    )
    def handle_next_precipitation(self, message: Message):
        """Handler for weather requests such as: when will it rain next?

        :param message: Message Bus event information from the intent parser
        """
        intent_data = WeatherIntent(message, self.lang)
        weather = self._get_weather(intent_data)
        if weather is not None:
            forecast, timeframe = weather.get_next_precipitation(intent_data)
            intent_data.timeframe = timeframe
            dialog = WeatherDialog(forecast, self.weather_config, intent_data)
            dialog.build_next_precipitation_dialog()
            self._speak_weather(dialog)

    @intent_handler(
        IntentBuilder("")
        .require("Query")
        .require("Humidity")
        .optionally("RelativeDay")
        .optionally("Location")
    )
    def handle_humidity(self, message: Message):
        """Handler for weather requests such as: how humid is it?

        :param message: Message Bus event information from the intent parser
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            dialog = WeatherDialog(intent_weather, self.weather_config, intent_data)
            dialog.build_humidity_dialog()
            dialog.data.update(
                humidity=self.translate(
                    "percentage.number", data=dict(num=dialog.data.humidity)
                )
            )
            self._speak_weather(dialog)

    @intent_handler(
        IntentBuilder("")
        .one_of("Query", "When")
        .optionally("Location")
        .require("Sunrise")
    )
    def handle_sunrise(self, message: Message):
        """Handler for weather requests such as: when is the sunrise?

        :param message: Message Bus event information from the intent parser
        """
        intent_data = WeatherIntent(message, self.lang)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            dialog = WeatherDialog(intent_weather, self.weather_config, intent_data)
            dialog.build_sunrise_dialog()
            self._speak_weather(dialog)

    @intent_handler(
        IntentBuilder("")
        .one_of("Query", "When")
        .optionally("Location")
        .require("Sunset")
    )
    def handle_sunset(self, message: Message):
        """Handler for weather requests such as: when is the sunset?

        :param message: Message Bus event information from the intent parser
        """
        intent_data = WeatherIntent(message, self.lang)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            dialog = WeatherDialog(intent_weather, self.weather_config, intent_data)
            dialog.build_sunset_dialog()
            self._speak_weather(dialog)

    def _report_current_weather(self, message: Message):
        """Handles all requests for current weather conditions.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            self._display_current_conditions(weather, intent_data)
            dialog = WeatherDialog(weather, self.weather_config, intent_data)
            dialog.build_current_weather_dialog()
            self._speak_weather(dialog)
            if self.gui.connected and self.platform != MARK_II:
                self._display_more_current_conditions(weather)
            dialog.build_high_low_temperature_dialog()
            self._speak_weather(dialog)
            if self.gui.connected:
                if self.platform == MARK_II:
                    self._display_more_current_conditions(weather)
                    sleep(5)
                    self._display_hourly_forecast(weather)
                else:
                    four_day_forecast = weather.daily[1:5]
                    self._display_forecast(four_day_forecast)

    def _display_current_conditions(self, weather: WeatherReport, intent_data: WeatherIntent):
        """Display current weather conditions on a screen.

        This is the first screen that shows.  Others will follow.

        :param weather: current weather conditions from Open Weather Maps
        """
        image_code = self.image_codes[weather.current.condition.icon]
        if self.gui.connected:
            page_name = "current_1_scalable.qml"
            self.gui.clear()
            self.gui["currentTemperature"] = weather.current.temperature
            self.gui["weatherCode"] = image_code
            if self.platform == MARK_II:
                self.gui["weatherLocation"] = self._build_display_location(intent_data)
                self.gui["highTemperature"] = weather.current.high_temperature
                self.gui["lowTemperature"] = weather.current.low_temperature
                page_name = page_name.replace("scalable", "mark_ii")
            self.gui.show_page(page_name)
        else:
            self.enclosure.deactivate_mouth_events()
            self.enclosure.weather_display(image_code, weather.current.temperature)

    def _build_display_location(self, intent_data: WeatherIntent) -> str:
        if intent_data.geolocation:
            location = [intent_data.geolocation["city"]]
            if intent_data.geolocation["country"] == self.weather_config.country:
                location.append(intent_data.geolocation["region"])
            else:
                location.append(intent_data.geolocation["country"])
        else:
            location = [self.weather_config.city, self.weather_config.state]

        return ", ".join(location)

    def _display_more_current_conditions(self, weather: WeatherReport):
        """Display current weather conditions on a device that supports a GUI.

        This is the second screen that shows for current weather.

        :param weather: current weather conditions from Open Weather Maps
        """
        page_name = "current_2_scalable.qml"
        self.gui.clear()
        if self.platform == MARK_II:
            self.gui["windSpeed"] = weather.current.wind_speed
            self.gui["humidity"] = weather.current.humidity
            page_name = page_name.replace("scalable", "mark_ii")
        else:
            self.gui["highTemperature"] = weather.current.high_temperature
            self.gui["lowTemperature"] = weather.current.low_temperature
        self.gui.show_page(page_name)

    def _report_one_hour_weather(self, message: Message):
        """Handles requests for a one hour forecast.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            forecast = weather.get_forecast_for_hour(intent_data)
            dialog = WeatherDialog(forecast, self.weather_config, intent_data)
            dialog.build_hourly_weather_dialog()
            self._speak_weather(dialog)

    def _display_hourly_forecast(self, weather: WeatherReport):
        """Display hourly forecast on a device that supports the GUI.

        On the Mark II this screen is the final for current weather.  It can
        also be shown when the hourly forecast is requested.

        :param weather: hourly weather conditions from Open Weather Maps
        """
        hourly_forecast = []
        for hour_count, hourly in enumerate(weather.hourly):
            if not hour_count:
                continue
            if hour_count > 4:
                break
            # TODO: make the timeframe aware of language/location settings
            if self.config_core['time_format'] == TWELVE_HOUR:
                # The datetime builtin returns hour in two character format.  Convert
                # to a integer and back again to remove the leading zero when present.
                hour = int(hourly.date_time.strftime("%I"))
                am_pm = hourly.date_time.strftime(" %p")
                formatted_time = str(hour) + am_pm
            else:
                formatted_time = hourly.date_time.strftime("%H:00")
            hourly_forecast.append(
                dict(
                    time=hourly.date_time.strftime(formatted_time),
                    precipitation=hourly.chance_of_precipitation,
                    temperature=hourly.temperature,
                    weatherCode=self.image_codes.get(hourly.condition.icon),
                )
            )
        self.gui.clear()
        self.gui["hourlyForecast"] = dict(hours=hourly_forecast)
        self.gui.show_page("hourly_mark_ii.qml")

    def _report_multi_day_forecast(self, message: Message, days: int):
        """Handles all requests for multiple day forecasts.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = WeatherIntent(message, self.lang)
        weather = self._get_weather(intent_data)
        if weather is not None:
            forecast = weather.daily[1 : days + 1]
            dialogs = self._build_forecast_dialogs(forecast, intent_data)
            self._display_forecast(forecast)
            for dialog in dialogs:
                self._speak_weather(dialog)

    def _report_one_day_forecast(self, message: Message):
        """Handles all requests for a single day forecast.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = WeatherIntent(message, self.lang)
        weather = self._get_weather(intent_data)
        if weather is not None:
            forecast = [weather.get_forecast_for_date(intent_data)]
            dialogs = self._build_forecast_dialogs(forecast, intent_data)
            self._display_forecast(forecast)
            for dialog in dialogs:
                self._speak_weather(dialog)

    def _report_weekend_forecast(self, message: Message):
        """Handles requests for a weekend forecast.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            forecast = weather.get_weekend_forecast()
            dialogs = self._build_forecast_dialogs(forecast, intent_data)
            self._display_forecast(forecast)
            for dialog in dialogs:
                self._speak_weather(dialog)

    def _build_forecast_dialogs(
        self, forecast: List[DailyWeather], intent_data: WeatherIntent
    ) -> List[WeatherDialog]:
        """
        Build the dialogs for each of the forecast days being reported to the user.

        :param forecast: daily forecasts to report
        :param intent_data: information about the intent that was triggered
        :return: one WeatherDialog instance for each day being reported.
        """
        dialogs = list()
        for forecast_day in forecast:
            dialog = WeatherDialog(forecast_day, self.weather_config, intent_data)
            dialog.build_daily_weather_dialog()
            dialogs.append(dialog)

        return dialogs

    def _display_forecast(self, forecast: List[DailyWeather]):
        """Display daily forecast data on devices that support the GUI.

        :param forecast: daily forecasts to display
        """
        if self.platform == MARK_II:
            self._display_forecast_mark_ii(forecast)
        else:
            self._display_forecast_scalable(forecast)

    def _display_forecast_mark_ii(self, forecast: List[DailyWeather]):
        """Display daily forecast data on a Mark II.

        The Mark II supports displaying four days of a forecast at a time.

        :param forecast: daily forecasts to display
        """
        page_name = "daily_mark_ii.qml"
        daily_forecast = []
        for day in forecast:
            daily_forecast.append(
                dict(
                    weatherCode=self.image_codes[day.condition.icon],
                    day=day.date_time.strftime("%a"),
                    highTemperature=day.temperature.high,
                    lowTemperature=day.temperature.low
                )
            )
        self.gui.clear()
        self.gui["dailyForecast"] = dict(days=daily_forecast[:4])
        self.gui.show_page(page_name)
        if len(forecast) > 4:
            sleep(20)
            self.gui.clear()
            self.gui["dailyForecast"] = dict(days=daily_forecast[4:])
            self.gui.show_page(page_name)

    def _display_forecast_scalable(self, forecast: List[DailyWeather]):
        """Display daily forecast data on GUI devices other than the Mark II.

        The generic layout supports displaying two days of a forecast at a time.

        :param forecast: daily forecasts to display
        """
        page_one_name = "daily_1_scalable.qml"
        page_two_name = page_one_name.replace("1", "2")
        display_data = []
        for day_number, day in enumerate(forecast):
            if day_number == 4:
                break
            display_data.append(
                dict(
                    weatherCode=self.image_codes[day.condition.icon],
                    highTemperature=day.temperature.high,
                    lowTemperature=day.temperature.low,
                    date=day.date_time.strftime("%a"),
                )
            )
        self.gui["forecast"] = dict(first=display_data[:2], second=display_data[2:])
        self.gui.show_page(page_one_name)
        sleep(5)
        self.gui.show_page(page_two_name)

    def _report_temperature(self, message: Message, temperature_type: str = None):
        """Handles all requests for a temperature.

        :param message: Message Bus event information from the intent parser
        :param temperature_type: current, high or low temperature
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            dialog = WeatherDialog(intent_weather, self.weather_config, intent_data)
            dialog.build_temperature_dialog(temperature_type)
            self._speak_weather(dialog)

    def _report_weather_condition(self, message: Message, condition: str):
        """Handles all requests for a specific weather condition.

        :param message: Message Bus event information from the intent parser
        :param condition: the weather condition specified by the user
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            dialog = self._build_condition_dialog(
                intent_weather, intent_data, condition
            )
            self._speak_weather(dialog)

    def _build_condition_dialog(
        self, weather, intent_data: WeatherIntent, condition: str
    ) -> WeatherDialog:
        """Builds a dialog for the requested weather condition.

        :param weather: Current, hourly or daily weather forecast
        :param intent_data: Parsed intent data
        :param condition: weather condition requested by the user
        """
        dialog = WeatherDialog(weather, self.weather_config, intent_data)
        intent_match = self.voc_match(weather.condition.category.lower(), condition)
        alternative_vocab = condition + "Alternatives"
        alternative = self.voc_match(weather.condition.category, alternative_vocab)
        dialog.build_condition_dialog(condition, intent_match, alternative)
        dialog.data.update(condition=self.translate(condition))

        return dialog

    def _report_wind(self, message: Message):
        """Handles all requests for a wind conditions.

        :param message: Message Bus event information from the intent parser
        """
        intent_data = self._get_intent_data(message)
        weather = self._get_weather(intent_data)
        if weather is not None:
            intent_weather = weather.get_weather_for_intent(intent_data)
            intent_weather.wind_direction = self.translate(
                intent_weather.wind_direction
            )
            dialog = WeatherDialog(intent_weather, self.weather_config, intent_data)
            dialog.build_wind_dialog()
            self._speak_weather(dialog)

    def _get_intent_data(self, message: Message) -> WeatherIntent:
        """Parse the intend data from the message into data used in the skill.

        :param message: Message Bus event information from the intent parser
        :return: parsed information about the intent
        """
        intent_data = None
        try:
            intent_data = WeatherIntent(message, self.lang)
        except ValueError:
            self.speak_dialog("cant.get.forecast")
        else:
            if self.voc_match(intent_data.utterance, "RelativeTime"):
                intent_data.timeframe = "hourly"
            elif self.voc_match(intent_data.utterance, "Later"):
                intent_data.timeframe = "hourly"
            elif self.voc_match(intent_data.utterance, "RelativeDay"):
                if not self.voc_match(intent_data.utterance, "Today"):
                    intent_data.timeframe = "daily"

        return intent_data

    def _get_weather(self, intent_data: WeatherIntent) -> WeatherReport:
        """Call the Open Weather Map One Call API to get weather information

        :param intent_data: Parsed intent data
        :return: An object representing the data returned by the API
        """
        weather = None
        if intent_data is not None:
            try:
                latitude, longitude = self._determine_weather_location(intent_data)
                weather = self.weather_api.get_weather_for_coordinates(
                    self.config_core.get("system_unit"), latitude, longitude
                )
            except HTTPError as api_error:
                self.log.exception("Weather API failure")
                self._handle_api_error(api_error)
            except LocationNotFoundError:
                self.log.exception("City not found.")
                self.speak_dialog(
                    "location.not.found", data=dict(location=intent_data.location)
                )
            except Exception:
                self.log.exception("Unexpected error retrieving weather")
                self.speak_dialog("cant.get.forecast")

        return weather

    def _handle_api_error(self, exception: HTTPError):
        """Communicate an error condition to the user.

        :param exception: the HTTPError returned by the API call
        """
        if exception.response.status_code == 401:
            self.bus.emit(Message("mycroft.not.paired"))
        else:
            self.speak_dialog("cant.get.forecast")

    def _determine_weather_location(
        self, intent_data: WeatherIntent
    ) -> Tuple[float, float]:
        """Determine latitude and longitude using the location data in the intent.

        :param intent_data: Parsed intent data
        :return: latitude and longitude of the location
        """
        if intent_data.location is None:
            latitude = self.weather_config.latitude
            longitude = self.weather_config.longitude
        else:
            latitude = intent_data.geolocation["latitude"]
            longitude = intent_data.geolocation["longitude"]

        return latitude, longitude

    def _speak_weather(self, dialog: WeatherDialog):
        """Instruct device to speak the contents of the specified dialog.

        :param dialog: the dialog that will be spoken
        """
        self.log.info("Speaking dialog: " + dialog.name)
        self.speak_dialog(dialog.name, dialog.data)
        mycroft.audio.wait_while_speaking()


def create_skill():
    """Boilerplate to invoke the weather skill."""
    return WeatherSkill()
