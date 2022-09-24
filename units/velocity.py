from units.base import make_compound_unit, make_compound_dimension
from units.length import Length, kilometers, meters, miles
from units.time import seconds, hours, Time

Velocity = make_compound_dimension({Length: 1, Time: -1}, "Velocity")

meters_per_second = make_compound_unit(Velocity, 1, {meters: 1, seconds: -1})
kilometers_per_hour = make_compound_unit(Velocity, 1000 / 3600, {kilometers: 1, hours: -1})
mph_scale = miles.scale / hours.scale
miles_per_hour = make_compound_unit(Velocity, mph_scale, {miles: 1, hours: -1})
