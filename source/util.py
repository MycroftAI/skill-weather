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
from datetime import datetime

import pytz

from mycroft.api import GeolocationApi
from mycroft.util.parse import extract_datetime


class LocationNotFoundError(ValueError):
    pass


def convert_to_local_datetime(timestamp, timezone):
    naive_datetime = datetime.fromtimestamp(timestamp)
    utc_datetime = pytz.utc.localize(naive_datetime)
    local_timezone = pytz.timezone(timezone)
    local_datetime = utc_datetime.astimezone(local_timezone)

    return local_datetime


def get_utterance_datetime(utterance, timezone=None, language=None):
    # Change timezone returned by extract_datetime from Local to UTC
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


def get_tz_info(timezone):
    return pytz.timezone(timezone)

def get_geolocation(location: str):
    geolocation_api = GeolocationApi()
    geolocation = geolocation_api.get_geolocation(location)

    if geolocation is None:
        raise LocationNotFoundError("Location {} is unknown".format(location))

    return geolocation


def get_time_period(intent_datetime):
    # Translate a specific time '9am' to period of the day 'morning'
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


def get_sequence_of_days(weather, condition_category):
    longest_sequence = []
    this_sequence = []
    last_in_sequence = 0
    for day_count, daily in enumerate(weather.daily):
        if daily.condition.catetory == condition_category:
            if not last_in_sequence or day_count == last_in_sequence + 1:
                this_sequence.append(daily)
                last_in_sequence += 1
            else:
                if 1 > len(this_sequence) > len(longest_sequence):
                    longest_sequence = this_sequence
                this_sequence = []
                last_in_sequence = day_count

    return longest_sequence
