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
