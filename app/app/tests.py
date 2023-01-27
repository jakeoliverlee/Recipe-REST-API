from django.test import SimpleTestCase
from app import calc
# Sample Test case

class CalcTests(SimpleTestCase):
    def test_add_numbers(self):
        res = calc.add(5, 6)

        self.assertEqual(res, 11)

class CalcTests(SimpleTestCase):
    def test_subtract_numbers(self):
        res = calc.substract(10, 3)
        self.assertEqual(res, 7)




