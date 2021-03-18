from datetime import timedelta

from mycroft.util.time import now_local
from .util import (
    get_utterance_datetime, get_geolocation, get_tz_info, LocationNotFoundError
)


class WeatherIntent:
    _geolocation = None
    _intent_datetime = None
    _location_datetime = None

    def __init__(self, message, language):
        self.utterance = message.data["utterance"]
        self.location = message.data.get("Location")
        self.language = language
        self.unit = message.data.get("Unit")
        self.timeframe = "current"

    @property
    def geolocation(self):
        if self._geolocation is None:
            if self.location is None:
                self._geolocation = dict()
            else:
                self._geolocation = get_geolocation(self.location)
                if self._geolocation["city"].lower() not in self.location.lower():
                    raise LocationNotFoundError(
                        self.location + " is not a city"
                    )

        return self._geolocation

    @property
    def intent_datetime(self):
        if self._intent_datetime is None:
            utterance_datetime = get_utterance_datetime(
                self.utterance,
                timezone=self.geolocation.get("timezone"),
                language=self.language
            )
            if utterance_datetime is not None:
                delta = utterance_datetime - self.location_datetime
                if int(delta / timedelta(days=1)) > 7:
                    raise ValueError("Weather forecasts only supported up to 7 days")
                if utterance_datetime.date() < self.location_datetime.date():
                    raise ValueError("Historical weather is not supported")
                self._intent_datetime = utterance_datetime
            else:
                self._intent_datetime = self.location_datetime

        return self._intent_datetime

    @property
    def location_datetime(self):
        if self._location_datetime is None:
            if self.location is None:
                self._location_datetime = now_local()
            else:
                tz_info = get_tz_info(self.geolocation["timezone"])
                self._location_datetime = now_local(tz_info)

        return self._location_datetime
