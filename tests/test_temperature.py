import pytest

from pyunitx._exceptions import UnitException
from pyunitx.temperature import (celsius,
                                 celsius_to_kelvin_absolute,
                                 kelvin,
                                 fahrenheit,
                                 kilokelvin, )


def test_celsius_to_absolute():
    c = celsius(25)
    k = celsius_to_kelvin_absolute(c)

    assert k == kelvin("298.15")


def test_f_to_absolute():
    f = fahrenheit(100)

    with pytest.raises(UnitException):
        celsius_to_kelvin_absolute(f)


def test_si_prefix():
    hot = kelvin(30122)
    cold = kelvin(266)

    assert hot.closest_si_prefix() == kilokelvin("30.122")
    assert cold.closest_si_prefix() == kelvin(266)
