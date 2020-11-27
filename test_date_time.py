"""
Test cases for datetime utils.
"""
from datetime import datetime, timedelta
from unittest import TestCase

import pytz
from pytz import timezone

from date_time import datetime_to_float, float_to_datetime, time_range_chunker


class TestDateTime(TestCase):
    """
    Test cases for datetime utils.
    """

    def test_datetime_to_float_timezone_aware(self):
        """
        2h into the epoch in CET is 1h into the epoch in UTC.
        Return a timezone-aware object.
        """
        cet_tz = timezone('CET')
        dt = datetime(1970, 1, 1, 2, 0, 0, 123000, tzinfo=cet_tz)
        ts_expected = 3600.123  # 123000 microseconds = 123 milliseconds
        ts_actual = datetime_to_float(dt)
        self.assertEqual(ts_expected, ts_actual)

    def test_datetime_to_float_timezone_aware_zero(self):
        """
        The epoch start in UTC sure equals ts=0.
        Return a timezone-aware object.
        """
        dt = datetime(1970, 1, 1, 0, 0, tzinfo=pytz.UTC)
        ts_expected = 0
        ts_actual = datetime_to_float(dt)
        self.assertEqual(ts_expected, ts_actual)

    def test_datetime_to_float_timezone_naive(self):
        """
        1h after the epoch begins.
        Return a timezone-naive object.
        """
        dt = datetime(1970, 1, 1, 2, 0)
        ts_expected = 3600 * 2
        ts_actual = datetime_to_float(dt)
        self.assertEqual(ts_expected, ts_actual)

    def test_float_to_datetime_naive(self):
        """
        Without timezone: ts=3600 is 1h after the epoch start.
        Return a timezone-naive object, assumed to be UTC.
        """
        input_ts = 3600
        expected_dt = datetime(1970, 1, 1, 1, 0, 0)  # 1h after epoch starts
        actual_dt = float_to_datetime(input_ts)
        self.assertEqual(expected_dt, actual_dt)

    def test_float_to_datetime_tz(self):
        """
        Epoch starts at 1am CET (midnight UTC). So 1h from that time is 2am CET, 1am UTC.
        Returns timezone-aware object.
        """
        cet_tz = timezone('CET')
        input_ts = 3600
        expected_dt_cet = datetime(1970, 1, 1, 2, 0, 0, tzinfo=cet_tz)
        expected_dt_utc = datetime(1970, 1, 1, 1, 0, 0, tzinfo=pytz.UTC)
        actual_dt = float_to_datetime(input_ts, tzinfo=cet_tz)
        self.assertEqual(expected_dt_cet, actual_dt)
        self.assertEqual(expected_dt_utc, actual_dt.astimezone(pytz.UTC))


class TestTimeRangeChunker(TestCase):
    def test_time_chunker(self):
        """
        Ensure the time chunker works as expected
        """
        start_date = datetime(2020, 10, 10, 15, 30)
        end_date = datetime(2020, 10, 13, 16, 35)  # 3 days, 1h, 5min later
        interval = timedelta(days=1)

        expected = [
            (datetime(2020, 10, 10, 15, 30), datetime(2020, 10, 11, 15, 30)),
            (datetime(2020, 10, 11, 15, 30), datetime(2020, 10, 12, 15, 30)),
            (datetime(2020, 10, 12, 15, 30), datetime(2020, 10, 13, 15, 30)),
            (datetime(2020, 10, 13, 15, 30), datetime(2020, 10, 13, 16, 35)),
        ]

        actual = list(time_range_chunker(start_date, end_date, interval))

        self.assertListEqual(expected, actual)

    def test_time_chunker_invalid_data(self):
        """
        Ensure the time chunker handles unnatural time ranges by returning None
        """
        t1 = datetime(2020, 10, 10)
        t2 = datetime(2020, 10, 11)

        self.assertListEqual(list(time_range_chunker(t1, t1)), [])
        self.assertListEqual(list(time_range_chunker(t2, t1)), [])
