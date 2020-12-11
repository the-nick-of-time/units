from unittest import TestCase

from base import make_dimension, make_unit, Decimal, make_compound_dimension, make_compound_unit
from exceptions import OperationError, ImplicitConversionError


class TestMakeDimension(TestCase):
    def test_self_reference(self):
        dim = make_dimension("TEST")
        self.assertIs(dim, dim.DIMENSION)


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


class TestCompoundDimension(TestCase):
    def setUp(self):
        self.dimA = make_dimension("FIRST")
        self.dimB = make_dimension("SECOND")
        self.unitA = make_unit("first", self.dimA, 1)
        self.unitB = make_unit("second", self.dimB, 1)

    def test_isinstance(self):
        a = make_compound_dimension("baseline", ((self.dimA, 1), (self.dimB, -1)))
        b = make_compound_dimension("compare", ((self.dimA, 1), (self.dimB, -1)))
        unit_a = make_unit("fromA", a, 1)

        self.assertTrue(unit_a(1).instance_of(a))
        self.assertTrue(unit_a(1).instance_of(b))


class TestCompoundUnit(TestCase):
    def setUp(self):
        self.simple_a = make_dimension("a")
        self.simple_b = make_dimension("b")
        self.dimension = make_compound_dimension("TEST", ((self.simple_a, 1),
                                                          (self.simple_b, -1)))
        self.alt_dimension = make_compound_dimension("TESTAlt", ((self.simple_a, 1),
                                                                 (self.simple_b, -2)))

    def test_add(self):
        unit = make_compound_unit(self.dimension, 1)
        a = unit(1)
        b = unit(2)
        expected = unit(3)

        self.assertIs(expected, a + b)

    def test_add_equivalent(self):
        pass

    def test_subtract(self):
        unit = make_compound_unit(self.dimension, 1)
        a = unit(5)
        b = unit(2)
        expected = unit(3)

        self.assertIs(expected, a - b)

    def test_subtract_equivalent(self):
        pass

    def test_multiply_scalar(self):
        unit = make_compound_unit(self.dimension, 1)
        a = unit(1)
        expected = unit(3)

        self.assertIs(expected, a * 3)

    def test_multiply_simple_unit(self):
        compound = make_compound_unit(self.dimension, 1)
        simple = make_unit("simple", self.simple_b, 1)
        expected_unit = make_unit('expected', self.simple_a, 1)

        expected = expected_unit(2)
        result = compound(2) * simple(1)

        self.assertTrue(result.instance_of(expected_unit))
        self.assertEqual(expected, result)

    def test_multiply_complex_unit(self):
        first = make_compound_unit(self.dimension, 1)
        second = make_compound_unit(self.alt_dimension, 1)

        expected_dim = make_compound_dimension("EXPECTED", ((self.simple_a, 2),
                                                            (self.simple_b, -3)))
        expected_unit = make_compound_unit(expected_dim, 1)

        expected = expected_unit(1)
        result = first(1) * second(1)

        self.assertTrue(result.instance_of(expected_dim))
        self.assertEqual(expected, result)

    def test_divide_scalar(self):
        unit = make_compound_unit(self.dimension, 1)
        a = unit(3)
        expected = unit(1)

        self.assertIs(expected, a / 3)

    def test_divide_simple_unit(self):
        a = make_unit("a", self.simple_a, 1)
        b = make_unit("b", self.simple_b, 1)
        expected_unit = make_compound_unit(self.dimension, 1)
        expected = expected_unit(1)

        result = a(1) / b(1)

        self.assertTrue(result.instance_of(expected_unit))
        self.assertEqual(expected, result)

    def test_divide_to_dimensionless(self):
        simple = make_unit("simple", self.simple_a, 1)
        expected = 2

        result = simple(4) / simple(2)

        self.assertEqual(expected, result)

    def test_divide_complex_unit(self):
        pass

    def test_unit_name(self):
        length = make_unit('Meters', self.dimension, 1)
        time = make_unit('Seconds', self.alt_dimension, 1)

        velocity = make_compound_dimension("Velocity", ((length, 1), (time, -1)))
        mps = make_compound_unit(velocity, 1)

        self.assertEqual("MetersPerSecond", mps.__name__)

    def test_unit_name_exponent(self):
        length = make_unit('Meters', self.dimension, 1)
        time = make_unit('Seconds', self.alt_dimension, 1)

        acceleration = make_compound_dimension("Acceleration", ((length, 1), (time, -2)))
        mpss = make_compound_unit(acceleration, 1)

        self.assertEqual("MetersPerSecondSquared", mpss.__name__)
