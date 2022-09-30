from decimal import Decimal

from pyunitx._api import make_dimension, make_unit, si_unit

Time = make_dimension("Time")
seconds = make_unit(
    name="seconds",
    dimension=Time,
    scale=1,
    abbrev="s",
    doc="""\
    The second is the SI base unit of time. As there are convenient larger 
    units for time already, the positive SI prefixes (k, M, G) aren't used very 
    much but the negative ones (m, μ, n) do see common use.
    """
)

generated = si_unit(
    base_unit=seconds,
    short_doc=""":class:`seconds` are the base unit."""
)
globals().update(generated)

minutes = make_unit(
    name="minutes",
    dimension=Time,
    scale=60,
    abbrev="min",
    doc="""One minute is sixty seconds."""
)
hours = make_unit(
    name="hours",
    dimension=Time,
    scale=60 * 60,
    abbrev="hr",
    doc="""One hour is sixty minutes."""
)
days = make_unit(
    name="days",
    dimension=Time,
    scale=60 * 60 * 24,
    abbrev="day",
    doc="""\
    A solar day is exactly 24 hours. The solar day is loosely defined as the 
    period between zeniths of the sun. 
    """
)
sidereal_days = make_unit(
    name="sidereal_days",
    dimension=Time,
    scale=60 * 60 * 23 + 60 * 56 + Decimal("4.091"),
    abbrev="day_sd",
    doc="""\
    While the earth is spinning, it is also orbiting the sun. The movement along
    the orbit over the course of the day means that the sun has moved backwards
    a bit so the earth has to do some extra rotation before the sun is in the 
    same place again. If you instead hovered above one of the poles with a fixed
    orientation, and tracked the time it took for the earth to rotate back into
    the same position, you would get the length of the sidereal day. This is a 
    little shorter than a solar day.
    """
)
julian_years = make_unit(
    name="julian_years",
    dimension=Time,
    scale=days.scale * Decimal("365.25"),
    abbrev="year_jul",
    doc="""\
    It's nice to have a definition of a year that doesn't vary with things like
    leap years, and the Julian year is that.
    """
)

__all__ = [
              "Time",
              "seconds", "minutes", "hours",
              "days", "sidereal_days",
              "julian_years",
          ] + list(generated.keys())
