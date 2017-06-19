import logging

logger = logging.getLogger(__name__)

DAY_SECONDS = 60*60*24
HOUR_SECONDS = 60*60
MINUTE_SECONDS = 60


def parse_duration(time_str):
    # go to DAYS in seconds
    MULTIPLIERS = [1, MINUTE_SECONDS, HOUR_SECONDS]
    time_parts = reversed(time_str.split(':'))
    time_parts = [float(tp) for tp in time_parts]

    seconds = 0.0
    for i in range(len(time_parts)):
        seconds = seconds + (MULTIPLIERS[i] * time_parts[i])

    return seconds


def duration_to_string(seconds):
    remaining = 0
    hours, remaining = divmod(remaining, HOUR_SECONDS)
    minutes, remaining = divmod(remaining, MINUTE_SECONDS)
    seconds = remaining

    # just show the minimun string, leave out zeros 00:00:00:01.1
    # to return 1.1

    result = ''
    if minutes == 0:
        result = "{minutes:0>2}:{seconds:0>2}"
        result = result.format(minutes=minutes, seconds=seconds)

    return result
