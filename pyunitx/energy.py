from pyunitx._api import make_compound_dimension, make_compound_unit
from pyunitx.length import Length, meters
from pyunitx.mass import Mass, kilograms
from pyunitx.time import seconds, Time

__all__ = [
    "Energy",
    "joules",
    "kilojoule",
    "calorie",
]

Energy = make_compound_dimension({Mass: 1, Length: 2, Time: -2}, "Energy")

joules = make_compound_unit(
    name="joules",
    scale=1,
    exponents={kilograms: 1, meters: 2, seconds: -2},
    abbrev="J",
    doc="""\
    The joule is the base unit of energy in the SI system. It is the amount of
    work done on an object by pushing it with a 1 N force for 1 m. 
    """
)
kilojoule = make_compound_unit(
    name="kilojoule",
    scale=1000,
    exponents=joules.composition.to_pairs(),
    abbrev="kJ",
    doc="""\
    Since the joule is a pretty small amount of energy, kilojoules see common 
    use.
    """
)
calorie = make_compound_unit(
    name="calorie",
    scale="4.184",
    exponents=joules.composition.to_pairs(),
    abbrev="cal",
    doc="""\
    This is the gram calorie, the amount of heat energy necessary to heat 1 gram
    of water by 1 \xb0C. Nutritional calories are 1000 times larger, using a 
    kilogram in the calculation instead.
    """
)
