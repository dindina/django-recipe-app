from django.test import SimpleTestCase
from app import calc


class CalTests(SimpleTestCase):

    def test_add(self):
        res = calc.add(5, 6)
        self.assertEquals(res, 11)
