"""Conversions between these units are deltas, as the systems have different zeros."""

from units.base import make_unit, make_dimension

__all__ = [
    "Temperature",
    "kelvin",
    "celsius",
    "fahrenheit",
    "rankine",
    "absolute_zero_celsius",
    "celsius_to_kelvin_absolute",
]

Temperature = make_dimension("Temperature")

kelvin = make_unit("kelvin", Temperature, 1)
celsius = make_unit("degrees celsius", Temperature, 1)
fahrenheit = make_unit("degrees fahrenheit", Temperature, 5 / 9)
rankine = make_unit("rankine", Temperature, 5 / 9)

absolute_zero_celsius = celsius("-273.15")


def celsius_to_kelvin_absolute(degc: celsius) -> kelvin:
    return (degc - absolute_zero_celsius).to_kelvin()
