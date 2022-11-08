import math
import re
import typing
from collections.abc import Sequence
from decimal import Decimal
from numbers import Number

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


@typing.overload
def from_dms(spec: str) -> degrees:
    ...


@typing.overload
def from_dms(spec: typing.Tuple[Number, Number, Number]) -> degrees:
    ...


@typing.overload
def from_dms(d: Number, m: Number, s: Number) -> degrees:
    ...


def from_dms(d, m=None, s=None):
    if m is not None and s is not None and isinstance(d, (Decimal, float, int)):
        return degrees(d) + arcminutes(m).to_degrees() + arcseconds(s).to_degrees()
    if isinstance(d, Sequence) and len(d) == 3:
        d, m, s = d
        return degrees(d) + arcminutes(m).to_degrees() + arcseconds(s).to_degrees()
    decimal = re.compile(r"^([+-]?\d+(\.\d+)?)°?$")
    match = re.match(decimal, d.strip())
    if match:
        return degrees(match.group(1))
    dms = re.compile(r"^(\d+)°\s*(\d+)[′']\s*(\d+(\.\d+)?)[″\"]$")
    match = re.match(dms, d.strip())
    if match:
        deg, mn, sc = match.group(1), match.group(2), match.group(3)
        return degrees(deg) + arcminutes(mn).to_degrees() + arcseconds(sc).to_degrees()
    raise ValueError(
        "Either call with three numbers or with a string containing decimal "
        "degrees or with a string in degrees-minutes-seconds notation."
        )


degrees.from_dms = staticmethod(from_dms)
