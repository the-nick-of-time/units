import math
from decimal import Decimal

from units.base import make_dimension, make_unit

__all__ = [
    "Angle",
    "degree",
    "arcminute",
    "arcsecond",
]

Angle = make_dimension("Angle")

# Radians are better to be defined as a base unit but are dimensionless
degree = make_unit("degree", Angle, 1)
arcminute = make_unit("arcminute", Angle, 1 / 60)
arcsecond = make_unit("arcsecond", Angle, 1 / 3600)


def __to_rad(deg):
    return deg.value * deg.scale * Decimal(math.pi) / 180


Angle.to_radians = __to_rad
