from units.base import make_dimension, make_unit

Mass = make_dimension("Mass")

kilograms = make_unit("kilograms", Mass, 1)

grams = make_unit("grams", Mass, "0.001")
av_pound = make_unit("avoirdupois_pounds_mass", Mass, "0.45359237")
troy_pound = make_unit("troy_pounds_mass", Mass, "0.3732417")
slug = make_unit("slug", Mass, "14.59390")
