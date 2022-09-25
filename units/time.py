from decimal import Decimal

from units.base import make_unit, make_dimension

__all__ = [
    "Time",
    "seconds", "minutes", "hours",
    "days", "sidereal_days",
    "julian_years",
]
Time = make_dimension("Time")
seconds = make_unit("seconds", Time, 1)

minutes = make_unit("minutes", Time, 60)
hours = make_unit("hours", Time, 60 * 60)
days = make_unit("days", Time, 60 * 60 * 24)
sidereal_days = make_unit("sidereal_days", Time, 60 * 60 * 23 + 60 * 56 + Decimal("4.091"))
julian_years = make_unit("julian years", Time, days.scale * Decimal("365.25"))
