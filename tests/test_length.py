import pytest

from pyunitx._api import make_compound_dimension
from pyunitx.area import hectares
from pyunitx.length import (kilometers,
                            meters,
                            feet,
                            inches,
                            yards,
                            Length,
                            micrometers,
                            millimeters,
                            angstroms, )


def test_km_to_m():
    km = kilometers(1)
    m = km.to_meters()
    assert m == meters(1000)


def test_ft_to_m():
    ft = feet(1)
    m = ft.to_meters()
    assert m == meters("0.3048")


def test_area_conversion():
    a = meters(2)
    b = feet("6.56168")
    assert (a * a).equivalent_to(b * b, 5)


def test_equivalent_different_dimension():
    with pytest.raises(TypeError):
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
    mag = (vec[0] ** 2 + vec[1] ** 2) ** ".5"

    assert mag == meters(5)


def test_flyweight():
    a = meters(1)
    b = meters(1)
    c = meters(2)
    d = meters(2)
    assert a is b
    assert a is not c
    assert c is d


def test_flyweight_types():
    a = meters(1000)
    b = meters("1e3")
    assert a is b


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


def test_abs():
    assert abs(meters(-4)) == meters(4)
    assert abs(meters(1)) == meters(1)


def test_negative():
    assert -meters(4) == meters(-4)
    assert -meters(-2) == meters(2)


def test_positive():
    assert +meters(2) == meters(2)
    assert +meters(-4) == meters(-4)


def test_equal_base_identical():
    km_in_m = meters(1000)
    km = kilometers(1)
    assert km == km_in_m.to_kilometers()


def test_equal_base_incompatible():
    km = kilometers(1)
    m = meters(1000)
    assert km != m


def test_add_base_identical():
    a = meters(1)
    b = meters(2)
    assert a + b == meters(3)


def test_add_base_incompatible():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(TypeError):
        print(a + b)
    with pytest.raises(TypeError):
        print(1 + a)


def test_subtract_base_identical():
    a = meters(5)
    b = meters(2)
    expected = meters(3)
    assert a - b == expected


def test_subtract_base_incompatible():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(TypeError):
        print(a - b)
    with pytest.raises(TypeError):
        print(1 - a)


@pytest.mark.parametrize(
    "a,b,expect", [
        (3, 5, True),
        (3, 3, False),
        (3, -4, False),
    ]
)
def test_less(a, b, expect):
    assert (meters(a) < meters(b)) == expect


def test_less_different():
    si = meters(1)
    imperial = feet(1)

    with pytest.raises(TypeError):
        print(si < imperial)


@pytest.mark.parametrize(
    "a,b,expect", [
        (3, 5, True),
        (3, 3, True),
        (3, -4, False),
    ]
)
def test_lesseq(a, b, expect):
    assert (meters(a) <= meters(b)) == expect


@pytest.mark.parametrize(
    "a,b,expect", [
        (3, 5, False),
        (3, 3, False),
        (3, -4, True),
    ]
)
def test_greater(a, b, expect):
    assert (meters(a) > meters(b)) == expect


@pytest.mark.parametrize(
    "a,b,expect", [
        (3, 5, False),
        (3, 3, True),
        (3, -4, True),
    ]
)
def test_greaterequal(a, b, expect):
    assert (meters(a) >= meters(b)) == expect


def test_si():
    large = meters(102364)
    small = meters("0.00004266")
    medium = meters("0.041")

    assert large.to_natural_si() == kilometers("102.364")
    assert small.to_natural_si() == micrometers("42.66")
    assert medium.to_natural_si() == millimeters(41)


def test_not_si():
    imperial = feet(10034)

    with pytest.raises(TypeError):
        imperial.to_natural_si()


def test_si_range():
    huge = meters("2.4e27")
    tiny = meters("8.1e-25")

    with pytest.raises(ValueError):
        huge.to_natural_si()

    with pytest.raises(ValueError):
        tiny.to_natural_si()


def test_si_unofficial():
    area = hectares(12345)

    with pytest.raises(TypeError):
        area.to_natural_si()


def test_format():
    precise = meters("987.654321")

    assert format(precise) == "987.654321 m"
    assert format(precise, ".2g") == "9.9E+2 m"
    assert format(precise, ".2G") == "9.9E+2 m"
    assert format(precise, ".6g") == "987.654 m"


def test_format_unsupported():
    precise = meters("987.654321")
    unsupported = [".3f", "%", ">+0"]
    for u in unsupported:
        with pytest.raises(ValueError):
            format(precise, u)


def test_exponential_scale():
    small = angstroms(1)
    assert small.to_meters() == meters("1e-10")
