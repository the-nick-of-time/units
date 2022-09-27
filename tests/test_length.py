import pytest

from units._api import make_compound_dimension
from units._exceptions import OperationError, ImplicitConversionError
from units.length import kilometers, meters, feet, inches, yards, Length


def test_km_to_m():
    km = kilometers(1)
    m = km.to_meters()
    assert m == meters(1000)


def test_ft_to_m():
    ft = feet(1)
    m = ft.to_meters()
    assert m == meters("0.3048")


def test_equal():
    km_in_m = meters(1000)
    km = kilometers(1)
    assert km == km_in_m.to_kilometers()


def test_equal_different_unit():
    km = kilometers(1)
    m = meters(1000)
    assert km != m


def test_add_same_unit():
    a = meters(1)
    b = meters(2)
    assert a + b == meters(3)


def test_add_different_unit():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(OperationError):
        print(a + b)


def test_subtract_same_unit():
    a = meters(5)
    b = meters(2)
    expected = meters(3)
    assert a - b == expected


def test_subtract_different_unit():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(OperationError):
        print(a - b)


def test_area_conversion():
    a = meters(2)
    b = feet("6.56168")
    assert (a * a).equivalent_to(b * b, 1e-4)


def test_equivalent_different_dimension():
    with pytest.raises(ImplicitConversionError):
        print(meters(4).equivalent_to(meters(2) ** 2))


def test_imperial():
    i = inches(36)
    f = feet(3)
    y = yards(1)

    assert i.equivalent_to(f)
    assert f.equivalent_to(y)


def test_tostring():
    val = kilometers(3)
    expected = "3 km"
    assert str(val) == expected


def test_sqrt():
    vec = [meters(4), meters(3)]
    mag = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)

    assert mag == meters(5)


def test_flyweight():
    a = meters(1)
    b = meters(1)
    c = meters(2)
    d = meters(2)
    assert a is b
    assert a is not c
    assert c is d


def test_conversion():
    assert kilometers(1).to_meters() == meters(1000)


def test_scalar_multiply():
    assert meters(1) * 3 == meters(3)


def test_scalar_divide():
    assert meters(5) / 5 == meters(1)


def test_is_dimension():
    square = make_compound_dimension(exponents=((Length, 2),))
    assert (meters(2) ** 2).is_dimension(square)


def test_divide_to_dimensionless():
    r = meters(2)
    c = meters(6)

    assert c / r == 3


def test_is_nondimension():
    assert not meters(1).is_dimension(object)
