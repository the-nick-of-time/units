from unittest import TestCase

from exceptions import OperationError
from length import kilometers, meters, feet


class TestLength(TestCase):
    def test_km_to_m(self):
        km = kilometers(1)
        m = km.to_meters()
        self.assertEqual(kilometers.scale, m.value)
        self.assertIs(meters, type(m))

    def test_ft_to_m(self):
        ft = feet(1)
        m = ft.to_meters()
        self.assertAlmostEqual(feet.scale, m.value, places=4)
        self.assertIs(meters, type(m))

    def test_equal(self):
        km_in_m = meters(1000)
        km = kilometers(1)
        self.assertEqual(km, km_in_m)

    def test_add_same_unit(self):
        a = meters(1)
        b = meters(2)
        expected = meters(3)
        self.assertEqual(expected, a + b)

    def test_add_different_unit(self):
        a = meters(1)
        b = kilometers(1)
        with self.assertRaises(OperationError):
            print(a + b)

    def test_subtract_same_unit(self):
        a = meters(5)
        b = meters(2)
        expected = meters(3)
        self.assertEqual(expected, a - b)

    def test_subtract_different_unit(self):
        a = meters(1)
        b = kilometers(1)
        with self.assertRaises(OperationError):
            print(a - b)
