from units._api import make_dimension, make_unit

__all__ = [
    "Length",
    "meters",
    "kilometers",
    "feet",
    "miles",
    "yards",
    "inches",
    "astronomical_unit",
    "au",
]

Length = make_dimension("Length")

meters = make_unit(
    name="meters",
    dimension=Length,
    scale=1,
    doc="""\
    Meters are the base SI unit of length. It is currently defined in terms of
    the speed of light.
    """
)

kilometers = make_unit(
    name="kilometers",
    dimension=Length,
    scale=1000,
    doc="""\
    One kilometer is 1000 meters.
    """
)
feet = make_unit(
    name="feet",
    dimension=Length,
    scale="0.3048",
    doc="""Feet are the base unit of length in the |ucs|."""
)
miles = make_unit(
    name="miles",
    dimension=Length,
    scale="1609.344",
    doc="""Miles are the long distance measure in the |ucs|."""
)
yards = make_unit(
    name="yards",
    dimension=Length,
    scale="0.9144",
    doc="""One yard is equal to three feet."""
)
inches = make_unit(
    name="inches",
    dimension=Length,
    scale="0.0254",
    doc="""Twelve inches make up one foot."""
)
astronomical_unit = au = make_unit(
    name="au",
    dimension=Length,
    scale=149_597_870_700,
    doc="""\
    One astronomical unit, or AU, is the average distance between Earth and the
    Sun. It's used in astronomical measurements, and is part of the definition
    of the :class:`parsec <units.derived.parsec>`.
    """
)
