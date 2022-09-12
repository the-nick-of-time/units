import pytest

from units.base import make_dimension, make_unit, Decimal, make_compound_dimension, \
    make_compound_unit
from units.exceptions import OperationError, ImplicitConversionError


@pytest.fixture
def dimension():
    return make_dimension("TEST")


@pytest.fixture
def dimension2():
    return make_dimension("TEST2")


@pytest.fixture
def compound_dimension(dimension, dimension2):
    return make_compound_dimension("COMPOUND", ((dimension, 1), (dimension2, -1)))


@pytest.fixture
def compound_dimension2(dimension, dimension2):
    return make_compound_dimension("COMPOUND2", ((dimension, 1), (dimension2, -2)))


def test_self_reference():
    dim = make_dimension("TEST")
    assert dim is dim.DIMENSION


def test_flyweights(dimension):
    unit = make_unit("testunit", dimension, Decimal("2"))
    a = unit(1)
    b = unit(1)
    c = unit(2)
    d = unit(2)
    assert a is b
    assert a is not c
    assert c is d


def test_conversion(dimension):
    first = make_unit("first", dimension, 1)
    second = make_unit("second", dimension, 10)
    ten_ones = first(10)
    one_ten = second(1)
    assert ten_ones.to_second() == one_ten


def test_add_same_unit(dimension):
    unit = make_unit("unit", dimension, 1)
    one = unit(1)
    two = unit(2)
    three = unit(3)
    assert three == one + two


def test_add_different_unit(dimension):
    first = make_unit("first", dimension, 1)
    second = make_unit("second", dimension, 10)
    a = first(10)
    b = second(1)
    with pytest.raises(OperationError):
        print(a + b)


def test_subtract_same_unit(dimension):
    unit = make_unit("unit", dimension, 1)
    one = unit(1)
    two = unit(2)
    three = unit(3)
    assert two == three - one


def test_subtract_different_unit(dimension):
    first = make_unit("first", dimension, 1)
    second = make_unit("second", dimension, 10)
    a = first(10)
    b = second(1)
    with pytest.raises(OperationError):
        print(a - b)


def test_equal_same_dimension(dimension):
    first = make_unit("first", dimension, 1)
    second = make_unit("second", dimension, 10)
    ten_ones = first(10)
    one_ten = second(1)
    assert ten_ones == one_ten


def test_equal_different_dimension(dimension):
    dim2 = make_dimension("dim2")
    first = make_unit("first", dimension, 1)
    a = first(1)
    second = make_unit("second", dim2, 1)
    b = second(1)
    with pytest.raises(ImplicitConversionError):
        print(a == b)


def test_multiply_scalar(dimension):
    unit = make_unit("unit", dimension, 1)
    one = unit(1)
    five = unit(5)
    assert five == one * 5


def test_divide_scalar(dimension):
    unit = make_unit("unit", dimension, 1)
    two = unit(2)
    four = unit(4)
    assert two == four / 2


def test_isinstance(dimension, dimension2):
    a = make_compound_dimension("baseline", ((dimension, 1), (dimension2, -1)))
    b = make_compound_dimension("compare", ((dimension, 1), (dimension2, -1)))
    unit_a = make_unit("fromA", a, 1)

    assert unit_a(1).instance_of(a)
    assert unit_a(1).instance_of(b)


def test_add(compound_dimension):
    unit = make_compound_unit(compound_dimension, 1)
    a = unit(1)
    b = unit(2)
    expected = unit(3)

    assert expected == a + b


def test_add_equivalent():
    pass


def test_subtract(compound_dimension):
    unit = make_compound_unit(compound_dimension, 1)
    a = unit(5)
    b = unit(2)
    expected = unit(3)

    assert expected == a - b


def test_subtract_equivalent():
    pass


def test_multiply_compound_scalar(compound_dimension):
    unit = make_compound_unit(compound_dimension, 1)
    a = unit(1)
    expected = unit(3)

    assert expected == a * 3


def test_multiply_simple_unit(compound_dimension, dimension, dimension2):
    compound = make_compound_unit(compound_dimension, 1)
    simple = make_unit("simple", dimension2, 1)
    expected_unit = make_unit('expected', dimension, 1)

    expected = expected_unit(2)
    result = compound(2) * simple(1)

    assert result.instance_of(expected_unit)
    assert expected == result


def test_multiply_complex_unit(compound_dimension, compound_dimension2, dimension, dimension2):
    first = make_compound_unit(compound_dimension, 1)
    second = make_compound_unit(compound_dimension2, 1)

    expected_dim = make_compound_dimension("EXPECTED", ((dimension, 2),
                                                        (dimension2, -3)))
    expected_unit = make_compound_unit(expected_dim, 1)

    expected = expected_unit(1)
    result = first(1) * second(1)

    assert result.instance_of(expected_dim)
    assert expected == result


def test_divide_compound_scalar(compound_dimension):
    unit = make_compound_unit(compound_dimension, 1)
    a = unit(3)
    expected = unit(1)

    assert expected == a / 3


def test_divide_simple_unit(dimension, dimension2, compound_dimension):
    a = make_unit("a", dimension, 1)
    b = make_unit("b", dimension2, 1)
    expected_unit = make_compound_unit(compound_dimension, 1)
    expected = expected_unit(1)

    result = a(1) / b(1)

    assert result.instance_of(expected_unit)
    assert expected == result


def test_divide_to_dimensionless(dimension):
    simple = make_unit("simple", dimension, 1)
    expected = 2

    result = simple(4) / simple(2)

    assert expected == result


def test_divide_complex_unit():
    pass


def test_unit_name(dimension, dimension2):
    length = make_unit('Meters', dimension, 1)
    time = make_unit('Seconds', dimension2, 1)

    velocity = make_compound_dimension("Velocity", ((length, 1), (time, -1)))
    mps = make_compound_unit(velocity, 1)

    assert "MetersPerSecond" == mps.__name__


def test_unit_name_exponent(dimension, dimension2):
    length = make_unit('Meters', dimension, 1)
    time = make_unit('Seconds', dimension2, 1)

    acceleration = make_compound_dimension("Acceleration", ((length, 1), (time, -2)))
    mpss = make_compound_unit(acceleration, 1)

    assert "MetersPerSecondSquared" == mpss.__name__
