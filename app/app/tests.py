from django.test import SimpleTestCase
from app import calc


class CalTests(SimpleTestCase):

    def test_add(self):
        res = calc.add(5, 6)
        self.assertEquals(res, 11)

    def test_sub(self):
        res = calc.subtract(7, 6)
        self.assertEquals(res, 1)
