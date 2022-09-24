from units.base import make_compound_unit, make_compound_dimension
from units.length import Length, meters
from units.mass import Mass, kilograms
from units.time import seconds, Time

Energy = make_compound_dimension({Mass: 1, Length: 2, Time: -2}, "Energy")

joules = make_compound_unit(Energy, 1, {kilograms: 1, meters: 2, seconds: -2}, "joules")
kilojoule = make_compound_unit(Energy, 1000, joules.composition.to_pairs(), "kilojoule")
calorie = make_compound_unit(Energy, "4.184", joules.composition.to_pairs(), "calorie")
