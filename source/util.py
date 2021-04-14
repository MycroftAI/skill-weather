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
"""Utility functions for the weather skill."""
from datetime import datetime, tzinfo
from time import time

import pytz

from mycroft.api import GeolocationApi
from mycroft.util.parse import extract_datetime


class LocationNotFoundError(ValueError):
    """Raise when the API cannot find the requested location."""

    pass


def convert_to_local_datetime(timestamp: time, timezone: str) -> datetime:
    """Convert a timestamp to a datetime object in the requested timezone.

    This function assumes it is passed a timestamp in the UTC timezone.  It
    then adjusts the datetime to match the specified timezone.

    :param timestamp: seconds since epoch
    :param timezone: the timezone requested by the user
    """
    naive_datetime = datetime.fromtimestamp(timestamp)
    utc_datetime = pytz.utc.localize(naive_datetime)
    local_timezone = pytz.timezone(timezone)
    local_datetime = utc_datetime.astimezone(local_timezone)

    return local_datetime


def get_utterance_datetime(
    utterance: str, timezone: str = None, language: str = None
) -> datetime:
    """Get a datetime representation of a date or time concept in an utterance.

    :param utterance: the words spoken by the user
    :param timezone: the timezone requested by the user
    :param language: the language configured on the device
    """
    utterance_datetime = None
    if timezone is None:
        anchor_date = None
    else:
        intent_timezone = get_tz_info(timezone)
        anchor_date = datetime.now(intent_timezone)
    extract = extract_datetime(utterance, anchor_date, language)
    if extract is not None:
        utterance_datetime, _ = extract

    return utterance_datetime


def get_tz_info(timezone: str) -> tzinfo:
    """Generate a tzinfo object from a timezone string.

    :param timezone: a string representing a timezone
    """
    return pytz.timezone(timezone)


def get_geolocation(location: str):
    """Retrieve the geolocation information about the requested location.

    :param location: a location specified in the utterance
    """
    geolocation_api = GeolocationApi()
    geolocation = geolocation_api.get_geolocation(location)

    if geolocation is None:
        raise LocationNotFoundError("Location {} is unknown".format(location))

    return geolocation


def get_time_period(intent_datetime: datetime) -> str:
    """Translate a specific time '9am' to period of the day 'morning'

    :param intent_datetime: the datetime extracted from an utterance
    """
    hour = intent_datetime.time().hour
    if 1 <= hour < 5:
        period = "early morning"
    elif 5 <= hour < 12:
        period = "morning"
    elif 12 <= hour < 17:
        period = "afternoon"
    elif 17 <= hour < 20:
        period = "evening"
    else:
        period = "overnight"

    return period
