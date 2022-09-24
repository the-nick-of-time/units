import pytest

from units.base import make_dimension, make_unit, Decimal, make_compound_dimension, \
    make_compound_unit
from units.exceptions import OperationError, ImplicitConversionError


@pytest.fixture
def dimension():
    return make_dimension("TEST")


@pytest.fixture
def unit(dimension):
    return make_unit('TESTUNIT', dimension, 1)


@pytest.fixture
def dimension2():
    return make_dimension("TEST2")


@pytest.fixture
def unit2(dimension2):
    return make_unit('TESTUNIT2', dimension2, 1)


@pytest.fixture
def compound_dimension(dimension, dimension2):
    return make_compound_dimension(((dimension, 1), (dimension2, -1)))


@pytest.fixture
def compound_unit(compound_dimension, unit, unit2):
    return make_compound_unit(compound_dimension, 1, ((unit, 1), (unit2, -1)))


@pytest.fixture
def compound_dimension2(dimension, dimension2):
    return make_compound_dimension(((dimension, 1), (dimension2, -2)))


@pytest.fixture
def compound_unit2(compound_dimension2, unit, unit2):
    return make_compound_unit(compound_dimension2, 1, ((unit, 1), (unit2, -2)))


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


def test_equivalent_same_dimension(dimension):
    first = make_unit("first", dimension, 1)
    second = make_unit("second", dimension, 10)
    ten_ones = first(10)
    one_ten = second(1)
    assert ten_ones.equivalent_to(one_ten)


def test_equivalence_different_dimension(dimension):
    dim2 = make_dimension("dim2")
    first = make_unit("first", dimension, 1)
    a = first(1)
    second = make_unit("second", dim2, 1)
    b = second(1)
    with pytest.raises(ImplicitConversionError):
        print(a.equivalent_to(b))


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
    a = make_compound_dimension(((dimension, 1), (dimension2, -1)), "baseline")
    b = make_compound_dimension(((dimension, 1), (dimension2, -1)), "compare")
    unit_a = make_unit("fromA", a, 1)

    assert unit_a(1).is_dimension(a)
    assert unit_a(1).is_dimension(b)


def test_add(compound_dimension, compound_unit):
    unit = make_compound_unit(compound_dimension, 1, compound_unit.composition.units, 'foo')
    a = unit(1)
    b = unit(2)
    expected = unit(3)

    assert expected == a + b


def test_add_equivalent():
    pass


def test_subtract(compound_dimension, compound_unit):
    unit = make_compound_unit(compound_dimension, 1, compound_unit.composition.units, 'foo')
    a = unit(5)
    b = unit(2)
    expected = unit(3)

    assert expected == a - b


def test_subtract_equivalent():
    pass


def test_multiply_compound_scalar(compound_dimension, compound_unit):
    unit = make_compound_unit(compound_dimension, 1, compound_unit.composition.units,
                              'multiply')
    a = unit(1)
    expected = unit(3)

    assert expected == a * 3


def test_multiply_simple_unit(compound_dimension, dimension, compound_unit, unit2):
    compound = make_compound_unit(compound_dimension, 1, compound_unit.composition.units,
                                  'multiply')
    expected_unit = make_unit('expected', dimension, 1)

    expected = expected_unit(2)
    result = compound(2) * unit2(1)

    assert result.is_dimension(dimension)
    assert result.equivalent_to(expected)


def test_multiply_complex_unit(dimension, dimension2,
                               compound_unit, compound_unit2, unit, unit2):
    expected_dim = make_compound_dimension(((dimension, 2),
                                            (dimension2, -3)), "EXPECTED")
    expected_unit = make_compound_unit(expected_dim, 1, ((unit, 2), (unit2, -3)),
                                       'EXPECTEDUNIT')

    expected = expected_unit(1)
    result = compound_unit(1) * compound_unit2(1)

    assert result.is_dimension(expected_dim)
    assert expected == result


def test_divide_compound_scalar(compound_dimension, compound_unit):
    unit = make_compound_unit(compound_dimension, 1, compound_unit.composition.units, 'foo')
    a = unit(3)
    expected = unit(1)

    assert expected == a / 3


def test_divide_simple_unit(compound_dimension, compound_unit, unit, unit2):
    expected = compound_unit(1)

    result = unit(1) / unit2(1)

    assert result.is_dimension(compound_dimension)
    assert expected == result


def test_divide_to_dimensionless(dimension):
    simple = make_unit("simple", dimension, 1)
    expected = 2

    result = simple(4) / simple(2)

    assert expected == result


def test_divide_complex_unit():
    pass


def test_dimension_auto_name(compound_dimension2):
    assert compound_dimension2.__name__ == "TEST_per_TEST2_squared"


def test_unit_auto_name(compound_unit):
    assert compound_unit.__name__ == "TESTUNIT_per_TESTUNIT2"
