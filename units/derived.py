from units.angle import arcsecond
from units.base import make_unit
from units.constants import c
from units.length import Length, au
from units.time import julian_years

parsec = make_unit("parsec", Length, au / arcsecond(1).to_radians())
lightyear = (c * julian_years(1))
