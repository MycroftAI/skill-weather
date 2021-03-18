from mycroft.util.format import nice_number, nice_time
from mycroft.util.time import now_local
from .util import get_time_period
from .weather import (
    is_current_weather, is_hourly_forecast, is_daily_forecast
)

CURRENT = "current"
DAILY = "daily"
HOURLY = "hourly"


# TODO: MISSING DIALOGS
#   - current.clear.alternative.local
#   - current.clouds.alternative.local
#   - daily.snow.alternative.local
#   - all hourly.<condition>.alternative.local/location
#   - all hourly.<condition>.not.expected.local/location
class WeatherDialog:
    def __init__(self, weather, config, intent_data):
        self.weather = weather
        self.config = config
        self.intent_data = intent_data
        self.current_weather = is_current_weather(weather)
        self.daily_forecast = is_daily_forecast(weather)
        self.hourly_forecast = is_hourly_forecast(weather)
        self.name = None
        self.data = None

    def build_current_weather_dialog(self):
        self.name = "current.weather"
        self.data = dict(
            condition=self.weather.condition.description,
            temperature=self.weather.temperature,
            temperature_unit=self.config.temperature_unit
        )
        self._add_location()

    def build_high_low_temperature_dialog(self):
        self.name = "current.temperature.high.low"
        self.data = dict(
            high_temperature=self.weather.high_temperature,
            low_temperature=self.weather.low_temperature
        )

    def build_hourly_weather_dialog(self):
        self.name = "hourly.weather"
        self.data = dict(
            condition=self.weather.condition.description,
            time=self.weather.date_time.strftime("%H:00"),
            temperature=self.weather.temperature,
        )
        self._add_location()

    def build_daily_weather_dialog(self):
        self.name = "daily.weather"
        self.data = dict(
            condition=self.weather.condition.description,
            day=self.weather.date_time.strftime("%A"),
            high_temperature=self.weather.temperature.high,
            low_temperature=self.weather.temperature.low
        )
        if self.weather.date_time.date() == self.intent_data.location_datetime.date():
            self.data.update(day="Today")
        self._add_location()

    def build_temperature_dialog(self, temperature_type):
        if self.daily_forecast:
            self._build_daily_temperature_dialog(temperature_type)
        elif self.hourly_forecast:
            self._build_hourly_temperature_dialog()
        else:
            self._build_current_temperature_dialog(temperature_type)
        self.data.update(
            temperature_unit=self.intent_data.unit or self.config.temperature_unit
        )
        self._add_location()

    def _build_current_temperature_dialog(self, temperature_type):
        self.name = "current.temperature"
        if temperature_type == "high":
            self.name += ".high"
            self.data = dict(temperature=self.weather.high_temperature)
        elif temperature_type == "low":
            self.name += ".low"
            self.data = dict(temperature=self.weather.low_temperature)
        else:
            self.data = dict(temperature=self.weather.temperature)

    def _build_daily_temperature_dialog(self, temperature_type):
        self.name = "daily.temperature"
        if temperature_type == "high":
            self.name += ".high"
            self.data = dict(temperature=self.weather.temperature.high)
        elif temperature_type == "low":
            self.name += ".low"
            self.data = dict(temperature=self.weather.temperature.low)
        else:
            self.data = dict(temperature=self.weather.temperature.day)
        self.data.update(day=self.weather.date_time.strftime('%A'))

    def _build_hourly_temperature_dialog(self):
        self.name = "hourly.temperature"
        self.data = dict(
            temperature=self.weather.temperature,
            time=get_time_period(self.weather.date_time)
        )

    def build_wind_dialog(self):
        wind_strength = self.weather.determine_wind_strength(
            self.config.speed_unit
        )
        self.data = dict(
            speed=nice_number(self.weather.wind_speed),
            speed_unit=self.config.speed_unit,
            direction=self.weather.wind_direction
        )
        self.name = self.intent_data.timeframe
        if self.intent_data.timeframe == DAILY:
            self.data.update(day=self.weather.date_time.strftime("%A"))
        elif self.hourly_forecast:
            self.data.update(time=nice_time(self.weather.date_time))
        self.name += '.wind.' + wind_strength
        self._add_location()

    def build_humidity_dialog(self):
        self.data = dict(percent=self.weather.humidity)
        if self.intent_data.timeframe == DAILY:
            self.name = "daily.humidity"
            self.data.update(day=self.weather.date_time.strftime("%A"))
        else:
            self.name = "current.humidity"
        self._add_location()

    def build_condition_dialog(self, condition, intent_match, alternative):
        """Select the relevant dialog file for condition based reports.

        A condition can for example be "snow" or "rain".

        Arguments:
            condition (string): name of condition eg snow

        Returns:
            dialog (string): name of dialog file
        """
        self.data = dict(condition=condition.lower())
        if self.daily_forecast:
            self.name = "daily"
            self.data.update(day=self.weather.date_time.strftime("%A"))
        elif self.hourly_forecast:
            self.name = "hourly"
            self.data.update(time=nice_time(self.weather.date_time))
        else:
            self.name = "current"
        if intent_match:
            self.name += ".condition.expected"
        elif alternative:
            self.name += ".{}.alternative".format(condition.lower())
        else:
            self.name += ".{}.not.expected".format(condition.lower())
        self._add_location()

    def build_next_precipitation_dialog(self):
        if self.weather is None:
            self.name = 'daily.precipitation.next.none'
            self.data = dict()
        else:
            if self.intent_data.timeframe == DAILY:
                self.name = 'daily.precipitation.next'
                self.data = dict(day=self.weather.date_time.strftime("%A"))
            else:
                self.name = 'hourly.precipitation.next'
                self.data = dict(time=get_time_period(self.weather.date_time))
            self.data = dict(
                percent=self.weather.chance_of_precipitation,
                precipitation="rain",
                day=self.weather.date_time.strftime("%A")
            )
        self._add_location()

    def build_sunrise_dialog(self):
        if self.daily_forecast:
            self.name = "daily.sunrise"
        else:
            if self.intent_data.location is None:
                now = now_local()
            else:
                now = now_local(tz=self.intent_data.geolocation["timezone"])
            if now < self.weather.sunrise:
                self.name = "current.sunrise.future"
            else:
                self.name = "current.sunrise.past"
        self._add_location()
        self.data = dict(time=nice_time(self.weather.sunrise.strftime("%H:%M")))

    def build_sunset_dialog(self):
        if self.daily_forecast:
            self.name = "daily.sunset"
        else:
            if self.intent_data.location is None:
                now = now_local()
            else:
                now = now_local(tz=self.intent_data.geolocation["timezone"])
            if now < self.weather.sunset:
                self.name = "current.sunset.future"
            else:
                self.name = "current.sunset.past"
        self._add_location()
        self.data = dict(time=nice_time(self.weather.sunset.strftime("%H:%M")))

    def _add_location(self):
        if self.intent_data.location is None:
            self.name += ".local"
        else:
            self.name += ".location"
            if self.config.country == self.intent_data.geolocation["country"]:
                spoken_location = ', '.join([
                    self.intent_data.geolocation["city"],
                    self.intent_data.geolocation["region"]
                ])
            else:
                spoken_location = ', '.join([
                    self.intent_data.geolocation["city"],
                    self.intent_data.geolocation["country"]
                ])
            self.data.update(location=spoken_location)
