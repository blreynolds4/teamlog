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


def remove_leading_zeros(time_str):
    parts = time_str.split(':')
    skip = True
    new_parts = []
    for p in parts:
        if skip and p in ['0', '00']:
            pass
        else:
            skip = False
            new_parts.append(p)

    return ':'.join(new_parts)
