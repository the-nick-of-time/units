from base import make_dimension, make_unit

Mass = make_dimension("Mass")

kilograms = make_unit("kilograms", Mass, 1)

grams = make_unit("grams", Mass, "0.001")
pounds = make_unit("pounds", Mass, "0.3732417216")
