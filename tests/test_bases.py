from unittest import TestCase

from base import make_dimension, make_unit, Decimal


class TestMakeDimension(TestCase):
    def test_construction(self):
        dim = make_dimension('TEST')
        self.assertIsNotNone(dim)


class TestMakeUnit(TestCase):
    def setUp(self):
        self.dimension = make_dimension('TEST')

    def test_flyweights(self):
        unit = make_unit('testunit', self.dimension, Decimal('2'))
        a = unit(1)
        b = unit(1)
        c = unit(2)
        d = unit(2)
        self.assertIs(a, b)
        self.assertIsNot(a, c)
        self.assertIs(c, d)

    def test_conversion(self):
        first = make_unit('first', self.dimension, Decimal('1'))
        second = make_unit('second', self.dimension, Decimal('10'))
        ten_ones = first(10)
        one_ten = second(1)
        # 'is' assumes that test_flyweights passed
        self.assertIs(ten_ones.to_second(), one_ten)
