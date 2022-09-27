import pytest

from pyunitx._exceptions import UnitException
from pyunitx.temperature import celsius, celsius_to_kelvin_absolute, kelvin, fahrenheit


def test_celsius_to_absolute():
    c = celsius(25)
    k = celsius_to_kelvin_absolute(c)

    assert k == kelvin("298.15")


def test_f_to_absolute():
    f = fahrenheit(100)

    with pytest.raises(UnitException):
        celsius_to_kelvin_absolute(f)
