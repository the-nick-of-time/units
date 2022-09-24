from units.base import make_dimension, make_unit

Angle = make_dimension("Angle")

# Radians are better to be defined as a base unit but are dimensionless
degree = make_unit("degree", Angle, 1)
arcminute = make_unit("arcminute", Angle, 1 / 60)
arcsecond = make_unit("arcsecond", Angle, 1 / 3600)
