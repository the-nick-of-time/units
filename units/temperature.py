"""Conversions between these units are deltas, as the systems have different units."""
from fractions import Fraction

from units.base import make_unit, make_dimension

Temperature = make_dimension("Temperature")

kelvin = make_unit("kelvin", Temperature, 1)
celsius = make_unit("degrees celsius", Temperature, 1)
fahrenheit = make_unit("degrees fahrenheit", Temperature, Fraction(5, 9))
rankine = make_unit("rankine", Temperature, Fraction(5, 9))
