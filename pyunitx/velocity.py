from pyunitx._api import make_compound_dimension, make_compound_unit
from pyunitx.length import Length, kilometers, meters, miles
from pyunitx.time import seconds, hours, Time

__all__ = [
    "Velocity",
    "meters_per_second",
    "kilometers_per_hour",
    "miles_per_hour",
]
Velocity = make_compound_dimension({Length: 1, Time: -1}, "Velocity")

meters_per_second = make_compound_unit(scale=1, exponents={meters: 1, seconds: -1})
kilometers_per_hour = make_compound_unit(
    scale=1000 / 3600,
    exponents={kilometers: 1, hours: -1}
)
mph_scale = miles.scale / hours.scale
miles_per_hour = make_compound_unit(scale=mph_scale, exponents={miles: 1, hours: -1})
