import pytest

from units._exceptions import OperationError
from units.length import kilometers, meters, feet, inches, yards


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


def test_imperial():
    i = inches(36)
    f = feet(3)
    y = yards(1)

    assert i.equivalent_to(f)
    assert f.equivalent_to(y)


def test_tostring():
    val = kilometers(3)
    expected = "3 kilometers"
    assert str(val) == expected


def test_sqrt():
    vec = [meters(4), meters(3)]
    mag = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)

    assert mag == meters(5)
