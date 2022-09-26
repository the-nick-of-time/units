from units import make_unit
from units.angle import arcsecond
from units.constants import c
from units.length import Length, au
from units.time import julian_years

__all__ = ["parsec", "lightyear"]

parsec_calc = au(1) / arcsecond(1).to_radians()
parsec = make_unit(name="parsec", dimension=Length, scale=parsec_calc.to_meters().value)
lightyear = make_unit(name="lightyear", dimension=Length, scale=c.value * julian_years.scale)
