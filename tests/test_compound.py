import pytest

from units._api import Compound, Multiset
from units._exceptions import ImplicitConversionError
from units.force import newtons
from units.length import meters, kilometers
from units.mass import kilograms
from units.temperature import kelvin
from units.time import seconds


def test_simple_pairs():
    c = Compound(((meters, 1), (seconds, -1)))
    assert c.to_pairs() == ((meters, 1), (seconds, -1))


def test_complex_pairs():
    c = Compound(((newtons, 1), (seconds, -1)))
    assert c.to_pairs() == ((kilograms, 1), (meters, 1), (seconds, -3))


def test_multiset():
    m = Multiset({meters: 1, kilograms: 1, seconds: -2})
    c = Compound(m)
    assert c.units is not m
    assert c.units.store is not m.store


def test_abbreviation():
    c = Compound(((kelvin, -1), (seconds, -2), (meters, 2), (kilograms, 1)))

    assert c.make_abbreviation() == "m^2 kg K^-1 s^-2"


def test_eq_non_compound():
    assert Compound(((meters, 1), (seconds, -1))) != {meters: 1, seconds: -1}


def test_len():
    c = Compound(((kelvin, -1), (seconds, -2), (meters, 2), (kilograms, 1)))

    assert len(c) == 4


def test_multiply():
    c1 = Compound(((meters, 1), (seconds, -1)))
    c2 = Compound(((newtons, 1),))
    expected = Compound(((seconds, -3), (meters, 2), (kilograms, 1)))

    assert c1 * c2 == expected


def test_multiply_single():
    c = Compound(((meters, 1), (seconds, -1)))
    expected = Compound(((meters, 1),))

    assert c * seconds == expected


def test_multiply_mismatch():
    c = Compound(((meters, 1), (seconds, -1)))

    with pytest.raises(ImplicitConversionError):
        print(c * kilometers)


def test_multiply_set():
    c = Compound(((meters, 1), (seconds, -1)))
    m = Multiset({meters: -2})

    assert c * m == Compound(((meters, -1), (seconds, -1)))


def test_divide():
    c1 = Compound(((newtons, 1),))
    c2 = Compound(((kilograms, 1), (meters, 1)))
    expected = Compound(((seconds, -2),))

    assert c1 / c2 == expected


def test_divide_single():
    c = Compound(((meters, 1), (seconds, -1)))
    expected = Compound(((seconds, -1),))

    assert c / meters == expected


def test_divide_mismatch():
    c = Compound(((meters, 1), (seconds, -1)))

    with pytest.raises(ImplicitConversionError):
        print(c / kilometers)


def test_divide_set():
    c = Compound(((meters, 1), (seconds, -1)))
    m = Multiset({meters: -2})

    assert c / m == Compound(((meters, 3), (seconds, -1)))


def test_pow_int():
    c = Compound(((meters, 1),))
    expected = Compound(((meters, 2),))

    assert c ** 2 == expected


def test_pow_sqrt():
    c = Compound(((meters, 2),))
    expected = Compound(((meters, 1),))

    assert c ** (1 / 2) == expected


def test_pow_sqrt_failure():
    c = Compound(((meters, 1),))

    with pytest.raises(ValueError):
        print(c ** (1 / 2))


def test_decompose():
    c = Compound(((newtons, 2),))

    assert c.to_pairs() == ((kilograms, 2), (meters, 2), (seconds, -4))
