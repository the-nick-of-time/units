"""Conversions between these units are deltas, as the systems have different zeros."""
from decimal import Decimal

from units import make_dimension, make_unit

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

kelvin = make_unit(name="kelvin", dimension=Temperature, scale=1, doc="""\
    Within this module, all temperatures are treated as deltas, ignoring the
    fact that the systems have different zeros. Thus, calling 
    ``celsius(25).to_kelvin()`` will *not* produce ``kelvin(298.15)`` as you
    might expect, but rather ``kelvin(25)``. To help out, the value of absolute
    zero has been provided in each of the non-absolute units.
    
    Kelvin is the absolute measure of temperature in the SI system.
    Its units are equal in size to the Celsius degree, but its zero point 
    is at absolute zero.""")
celsius = make_unit(name="celsius", dimension=Temperature, scale=1, doc="""\
    Within this module, all temperatures are treated as deltas, ignoring the
    fact that the systems have different zeros. Thus, calling 
    ``celsius(25).to_kelvin()`` will *not* produce ``kelvin(298.15)`` as you
    might expect, but rather ``kelvin(25)``. To help out, the value of absolute
    zero has been provided in each of the non-absolute units.
    
    To convert from a direct measurement in degrees Celsius to one in Kelvin,
    use ``(<celsius measurement> - absolute_zero_celsius).to_kelvin()``.
    The ``to_kelvin`` at the end is of course not strictly necessary, depending
    on how you are interpreting the results, but is certainly in line with 
    intention.
    """)
fahrenheit = make_unit(name="fahrenheit", dimension=Temperature, scale=Decimal(5) / 9)
rankine = make_unit(name="rankine", dimension=Temperature, scale=Decimal(5) / 9)

absolute_zero_celsius = celsius("-273.15")
absolute_zero_fahrenheit = fahrenheit("-459.67")


def celsius_to_kelvin_absolute(degc: celsius) -> kelvin:
    return (degc - absolute_zero_celsius).to_kelvin()
