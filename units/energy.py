from units.base import make_compound_unit, make_compound_dimension
from units.length import Length, meters
from units.mass import Mass, kilograms
from units.time import seconds, Time

__all__ = [
    "Energy",
    "joules",
    "kilojoule",
    "calorie",
]

Energy = make_compound_dimension({Mass: 1, Length: 2, Time: -2}, "Energy")

joules = make_compound_unit(scale=1, exponents={kilograms: 1, meters: 2, seconds: -2},
                            name="joules")
kilojoule = make_compound_unit(scale=1000, exponents=joules.composition.to_pairs(),
                               name="kilojoule")
calorie = make_compound_unit(scale="4.184", exponents=joules.composition.to_pairs(),
                             name="calorie")
