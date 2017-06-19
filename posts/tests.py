from django.test import TestCase
from .parsing import parse_duration
from .models import RunPost


class TimeParsingTest(TestCase):
    def test_parse_min_secs(self):
        seconds = parse_duration("5:44.3")
        self.assertEqual(344.3, seconds)

    def test_parse_secs(self):
        seconds = parse_duration("44.3")
        self.assertEqual(44.3, seconds)

    def test_parse_hms(self):
        seconds = parse_duration("3:07:11")
        self.assertEqual(11231, seconds)

    def test_time_to_str(self):
        p = RunPost(duration=44.3)

        actual = p._remove_leading_zeros("44.3")
        self.assertEqual("44.3", actual)

    def test_time_to_str_single_padded(self):
        p = RunPost(duration=44.3)

        actual = p._remove_leading_zeros("0:0:44.3")
        self.assertEqual("44.3", actual)

    def test_time_to_str_double_padded(self):
        p = RunPost(duration=44.3)

        actual = p._remove_leading_zeros("00:00:44.3")
        self.assertEqual("44.3", actual)

    def test_time_to_str_trickeration(self):
        p = RunPost(duration=44.3)

        actual = p._remove_leading_zeros("00:01:00:44.3")
        self.assertEqual("01:00:44.3", actual)
