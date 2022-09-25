from units.base import make_dimension, make_unit

__all__ = ["Mass", "kilograms", "av_pound", "troy_pound", "slug", "grams"]

Mass = make_dimension("Mass")

kilograms = make_unit("kilograms", Mass, 1)
grams = make_unit("grams", Mass, "0.001")
av_pound = make_unit("avoirdupois pounds_mass", Mass, "0.45359237")
troy_pound = make_unit("troy pounds_mass", Mass, "0.3732417")
slug = make_unit("slug", Mass, "14.59390")
