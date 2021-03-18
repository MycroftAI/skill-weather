from datetime import datetime
from typing import Optional

import pytz

from mycroft.api import GeolocationApi
from mycroft.util.format import nice_time
from mycroft.util.parse import extract_datetime
from mycroft.util.time import now_local, to_utc


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
# def get_spoken_time(date):
#     # compatibility wrapper for nice_time
#     nt_supported_languages = ['en', 'es', 'it', 'fr', 'de',
#                               'hu', 'nl', 'da']
#     if not (lang[0:2] in nt_supported_languages):
#         lang = "en-us"
#     return nice_time(dt, lang, speech, use_24hour, use_ampm)


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
