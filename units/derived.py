from units.angle import arcsecond
from units.base import make_unit
from units.length import Length, au

parsec = make_unit("parsec", Length, au / arcsecond(1).to_radians())
