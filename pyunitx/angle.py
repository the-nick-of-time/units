import math
from decimal import Decimal

from pyunitx._api import make_dimension, make_unit

__all__ = [
    "Angle",
    "degrees",
    "arcminutes",
    "arcseconds",
]

Angle = make_dimension("Angle")

# Radians are better to be defined as a base unit but are dimensionless
degrees = make_unit(
    name="degrees",
    dimension=Angle,
    scale=1,
    abbrev="\xb0",
    doc="""\
    Degrees are a measure of angles. 360 degrees extend around a circle. The 
    true base unit of angle is the dimensionless radian, but degrees see common 
    use as well.
    
    All angle measurements in this module are equipped with a to_radians 
    method alongside the other conversion functions that work between the angle
    measurements defined here. 
    """
)
arcminutes = make_unit(
    name="arcminutes",
    dimension=Angle,
    scale=Decimal(1) / 60,
    abbrev="\u2032",
    doc="""An arcminute is 1/60 of a degree."""
)
arcseconds = make_unit(
    name="arcseconds",
    dimension=Angle,
    scale=Decimal(1) / 3600,
    abbrev="\u2033",
    doc="""An arcsecond is 1/60 of an arcminute, and therefore 1/3600 of a degree."""
)


def __to_rad(deg):
    return deg.value * deg.scale * Decimal(math.pi) / 180


def __from_rad(rad):
    return degrees(rad * 180 / math.pi)


degrees.from_radians = staticmethod(__from_rad)

Angle.to_radians = __to_rad
