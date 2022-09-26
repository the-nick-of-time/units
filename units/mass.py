from units import make_dimension, make_unit

__all__ = ["Mass", "kilograms", "av_pound", "troy_pound", "slug", "grams"]

Mass = make_dimension("Mass")

kilograms = make_unit(name="kilograms", dimension=Mass, scale=1)
grams = make_unit(name="grams", dimension=Mass, scale="0.001")
av_pound = make_unit(name="avoirdupois_pounds_mass", dimension=Mass, scale="0.45359237")
troy_pound = make_unit(name="troy_pounds_mass", dimension=Mass, scale="0.3732417")
slug = make_unit(name="slug", dimension=Mass, scale="14.59390")
