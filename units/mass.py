from decimal import Decimal

from base import make_dimension, make_unit

Mass = make_dimension("Mass")

kilograms = make_unit("kilograms", Mass, 1)
Mass.BASE_UNIT = kilograms

grams = make_unit("grams", Mass, Decimal("0.001"))
pounds = make_unit("pounds", Mass, Decimal("0.3732417216"))
