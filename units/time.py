from decimal import Decimal

from units.base import make_unit, make_dimension, make_compound_dimension, make_compound_unit

__all__ = [
    "Time",
    "seconds", "minutes", "hours",
    "days", "sidereal_days",
    "julian_years",
    "Frequency",
    "hertz",
    "rpm",
]
Time = make_dimension("Time")
seconds = make_unit(name="seconds", dimension=Time, scale=1)

minutes = make_unit(name="minutes", dimension=Time, scale=60)
hours = make_unit(name="hours", dimension=Time, scale=60 * 60)
days = make_unit(name="days", dimension=Time, scale=60 * 60 * 24)
sidereal_days = make_unit(name="sidereal_days", dimension=Time,
                          scale=60 * 60 * 23 + 60 * 56 + Decimal("4.091"))
julian_years = make_unit(name="julian years", dimension=Time,
                         scale=days.scale * Decimal("365.25"))

Frequency = make_compound_dimension({Time: -1}, "Frequency")
hertz = make_compound_unit(scale=1, exponents={seconds: -1}, name="hertz")
rpm = make_compound_unit(scale=1 / 60, exponents={minutes: -1}, name="rpm")
