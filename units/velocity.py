import units.length as length
import units.time as time
from units.base import make_compound_unit, make_compound_dimension

Velocity = make_compound_dimension("Velocity", ((length.Length, 1), (time.Time, -1)))

meters_per_second = make_compound_unit("MetersPerSecond", Velocity, 1,
                                       ((length.meters, 1), (time.seconds, -1)))
kilometers_per_hour = make_compound_unit("KilometersPerHour", Velocity, 1000 / 3600,
                                         ((length.kilometers, 1), (time.hours, -1)))
mph_scale = length.miles.scale / time.hours.scale
miles_per_hour = make_compound_unit("MilesPerHour", Velocity, mph_scale,
                                    ((length.miles, 1), (time.hours, -1)))
