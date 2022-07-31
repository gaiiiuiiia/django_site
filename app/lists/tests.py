from django.test import TestCase


class SmokeTest(TestCase):
    def test_bad_math(self) -> None:
        self.assertEqual(1, 2)
