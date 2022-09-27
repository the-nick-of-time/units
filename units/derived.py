from units._api import make_unit
from units.angle import arcsecond
from units.constants import c
from units.length import Length, au
from units.time import julian_years

__all__ = ["parsec", "lightyear"]

parsec_calc = au(1) / arcsecond(1).to_radians()
parsec = make_unit(
    name="parsec",
    dimension=Length,
    scale=parsec_calc.to_meters().value,
    doc="""\
    One parsec is an astronomical distance defined by observation of the stars.
    As we orbit the sun, nearer stars move with respect to the extremely distant
    ones, an effect called parallax. Since we know the distance from the earth
    to the sun, we can calculate the distance the distance to those stars
    with a little trigonometry.
    
    If a star moves across an angle of one 
    :class:`arcsecond <units.angle.arcsecond>` as we observe it at either end of
    a distance of 1 AU, that means it is one parsec away. 
    """
)
lightyear = make_unit(
    name="lightyear",
    dimension=Length,
    scale=c.value * julian_years.scale,
    doc="""\
    A lightyear is the distance light travels in one year.
    As the real duration of a year changes over time (we're not going to say a
    lightyear is a different distance in a leap year) it uses a constant value
    of a Julian year, or 365.25 days.
    """
)
