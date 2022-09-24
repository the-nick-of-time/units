import fractions
import math

from units.base import make_dimension, make_unit

Angle = make_dimension("Angle")

# Radians are better to be defined as a base unit but are dimensionless
degree = make_unit("degree", Angle, 1)
arcminute = make_unit("arcminute", Angle, fractions.Fraction(1, 60))
arcsecond = make_unit("arcsecond", Angle, fractions.Fraction(1, 3600))


def __to_rad(deg):
    return deg.value * deg.scale * math.pi / 180


Angle.to_radians = __to_rad
