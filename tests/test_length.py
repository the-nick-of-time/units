from unittest import TestCase

from length import *


class TestLength(TestCase):
    def test_km_to_m(self):
        km = Kilometers(1)
        m = km.to_meters()
        self.assertEqual(Kilometers.scale, m.value)
        self.assertIs(Meters, type(m))

    def test_ft_to_m(self):
        ft = Feet(1)
        m = ft.to_meters()
        self.assertAlmostEqual(Feet.scale, m.value, places=4)
        self.assertIs(Meters, type(m))

    def test_equal(self):
        km_in_m = Meters(1000)
        km = Kilometers(1)
        self.assertEqual(km, km_in_m)

    def test_add_same_unit(self):
        a = Meters(1)
        b = Meters(2)
        expected = Meters(3)
        self.assertEqual(expected, a + b)

    def test_add_different_unit(self):
        a = Meters(1)
        b = Kilometers(1)
        with self.assertRaises(OperationError):
            a + b

    def test_subtract_same_unit(self):
        a = Meters(5)
        b = Meters(2)
        expected = Meters(3)
        self.assertEqual(expected, a - b)

    def test_subtract_different_unit(self):
        a = Meters(1)
        b = Kilometers(1)
        with self.assertRaises(OperationError):
            a - b
