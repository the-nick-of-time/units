import math
from decimal import Decimal

from units._api import make_dimension, make_unit

__all__ = [
    "Angle",
    "degree",
    "arcminute",
    "arcsecond",
]

Angle = make_dimension("Angle")

# Radians are better to be defined as a base unit but are dimensionless
degree = make_unit(name="degree", dimension=Angle, scale=1)
arcminute = make_unit(name="arcminute", dimension=Angle, scale=Decimal(1) / 60)
arcsecond = make_unit(name="arcsecond", dimension=Angle, scale=Decimal(1) / 3600)


def __to_rad(deg):
    return deg.value * deg.scale * Decimal(math.pi) / 180


Angle.to_radians = __to_rad
