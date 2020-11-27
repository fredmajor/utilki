"""
Datetime related utilities.
"""
import pytz
from datetime import datetime, timedelta


def datetime_to_float(d):
    """
    Convert a datetime object to a floating point timestamp.
    Return a number of seconds elapsed from UTC epoch.

    If the input object is timezone-aware, the result includes timezone difference between UTC
    and the timezone.
    If the input object is timezone-naive, it's treated as UTC.

    For example, 2h into the epoch in CET is 1h into the epoch in UTC (CET = UTC + 1h), so:
    >> cet_tz = timezone('CET')
    >> dt = datetime(1970, 1, 1, 2, 0, 0, tzinfo=cet_tz)
    >> datetime_to_float(dt)
    3600.0

    In case of a timezone-naive object, we treat the input as UTC, so:
    >> dt = datetime(1970, 1, 1, 2, 0)
    >> ts_expected = 3600 * 2
    >> datetime_to_float(dt)
    7200.0

    See tests for more examples.

    Args:
        d (datetime): can be timezone-aware or not

    Returns:
        float: e.g. 123456.123, always counting from UTC
    """
    epoch = datetime.fromtimestamp(0, tz=pytz.UTC)
    if not d.tzinfo:
        epoch = epoch.replace(tzinfo=None)

    total_seconds = (d - epoch).total_seconds()
    return total_seconds


def float_to_datetime(timestamp, tzinfo=None):
    """
    Convert a timestamp to a datetime instance.
    If tzinfo is passed, interpret the timestamp in the given timezone.
    If tzinfo isn't passed, interpret the timestamp as UTC.

    For example, epoch starts at 1am CET (midnight UTC, as CET = UTC + 1h). So 1h from that time is
    2am CET.
    >> cet_tz = timezone('CET')
    >> float_to_datetime(3600, tzinfo=cet_tz)
    datetime.datetime(1970, 1, 1, 2, 0, tzinfo=<DstTzInfo 'CET' CET+1:00:00 STD>)

    Without timezone give, 3600s from the epoch start is just 1h into the epoch:
    >> float_to_datetime(3600)
    datetime.datetime(1970, 1, 1, 1, 0)

    See tests for more examples.

    Args:
        timestamp (float): e.g. 123456.123, seconds from the epoch, can include milliseconds
        tzinfo (timezone): optional timezone object

    Returns:
        datetime: if no timezone given - a timezone-naive datetime.
                  Otherwise - a datetime object in the given timezone.
    """
    _tz = tzinfo if tzinfo else pytz.UTC
    dt = datetime.fromtimestamp(timestamp, tz=_tz)

    if not tzinfo:
        dt = dt.replace(tzinfo=None)
    return dt


def time_range_chunker(start_date, end_date, interval=timedelta(days=1)):
    """
    Generator. Splits a time range given by `start_date` and `end_date` into
    chunks of length specified by `interval`. Last chunk has duration <= interval.

    E.g. given:
    start_date = 2020-10-10 15:30:00,
    end_date   = 2020-10-12 16:35:00,
    interval   = 1 day

    it produces a following sequence of 3 tuples:
    (2020-10-10 15:30:00, 2020-10-11 15:30:00)
    (2020-10-11 15:30:00, 2020-10-12 15:30:00)
    (2020-10-12 15:30:00, 2020-10-12 16:35:00)

    Args:
        start_date (datetime): time range start
        end_date (datetime): time range end, has to be after the start_date
        interval (timedelta): single chunk interval
    """
    # gracefully ignore unnatural cases
    if not end_date > start_date:
        return

    chunk_start = chunk_end = start_date
    while chunk_end < end_date:
        chunk_end = chunk_start + interval
        if chunk_end > end_date:
            chunk_end = end_date
        yield chunk_start, chunk_end
        chunk_start = chunk_end
