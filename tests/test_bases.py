from unittest import TestCase

from base import make_dimension, make_unit, Decimal
from exceptions import OperationError, ImplicitConversionError


class TestMakeDimension(TestCase):
    def test_construction(self):
        dim = make_dimension("TEST")
        self.assertIsNotNone(dim)


class TestMakeUnit(TestCase):
    def setUp(self):
        self.dimension = make_dimension("TEST")

    def test_flyweights(self):
        unit = make_unit("testunit", self.dimension, Decimal("2"))
        a = unit(1)
        b = unit(1)
        c = unit(2)
        d = unit(2)
        self.assertIs(a, b)
        self.assertIsNot(a, c)
        self.assertIs(c, d)

    def test_conversion(self):
        first = make_unit("first", self.dimension, 1)
        second = make_unit("second", self.dimension, 10)
        ten_ones = first(10)
        one_ten = second(1)
        # "is" assumes that test_flyweights passed
        self.assertIs(ten_ones.to_second(), one_ten)

    def test_add_same_unit(self):
        unit = make_unit("unit", self.dimension, 1)
        one = unit(1)
        two = unit(2)
        three = unit(3)
        self.assertIs(three, one + two)

    def test_add_different_unit(self):
        first = make_unit("first", self.dimension, 1)
        second = make_unit("second", self.dimension, 10)
        a = first(10)
        b = second(1)
        with self.assertRaises(OperationError):
            print(a + b)

    def test_subtract_same_unit(self):
        unit = make_unit("unit", self.dimension, 1)
        one = unit(1)
        two = unit(2)
        three = unit(3)
        self.assertIs(two, three - one)

    def test_subtract_different_unit(self):
        first = make_unit("first", self.dimension, 1)
        second = make_unit("second", self.dimension, 10)
        a = first(10)
        b = second(1)
        with self.assertRaises(OperationError):
            print(a - b)

    def test_equal_same_dimension(self):
        first = make_unit("first", self.dimension, 1)
        second = make_unit("second", self.dimension, 10)
        ten_ones = first(10)
        one_ten = second(1)
        self.assertEqual(ten_ones, one_ten)

    def test_equal_different_dimension(self):
        dim2 = make_dimension("dim2")
        first = make_unit("first", self.dimension, 1)
        a = first(1)
        second = make_unit("second", dim2, 1)
        b = second(1)
        with self.assertRaises(ImplicitConversionError):
            print(a == b)

    def test_multiply_scalar(self):
        unit = make_unit("unit", self.dimension, 1)
        one = unit(1)
        five = unit(5)
        self.assertIs(five, one * 5)

    def test_divide_scalar(self):
        unit = make_unit("unit", self.dimension, 1)
        two = unit(2)
        four = unit(4)
        self.assertIs(two, four / 2)
