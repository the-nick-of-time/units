import units.length as length
import units.mass as mass
import units.time as time
from units.base import make_compound_unit, make_compound_dimension

Energy = make_compound_dimension(((mass.Mass, 1), (length.Length, 2), (time.Time, -2)),
                                 "Energy")

joule = make_compound_unit(Energy, 1,
                           ((mass.kilograms, 1), (length.meters, 2), (time.seconds, -2)),
                           "joule")
kilojoule = make_compound_unit(Energy, 1000, joule.composition.to_pairs(), "kilojoule")
calorie = make_compound_unit(Energy, "4.184", joule.composition.to_pairs(), "calorie")
