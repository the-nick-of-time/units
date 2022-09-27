from pyunitx._api import make_compound_dimension, make_compound_unit
from pyunitx.length import Length, meters, feet

__all__ = [
    "meters_cubed",
    "liters",
    "milliliters",
    "feet_cubed",
    "fluid_ounce",
    "cups",
    "teaspoon",
    "tablespoon"
]
Volume = make_compound_dimension({Length: 3}, "Volume")

meters_cubed = make_compound_unit(
    scale=1,
    exponents={meters: 3}
)
liters = make_compound_unit(
    name="liters",
    scale="1e-3",
    exponents={meters: 3},
    abbrev="L",
    doc="""\
    A liter is one cubic decimeter, or a cube about as big as the palm of your 
    hand.
    """
)
milliliters = make_compound_unit(
    name="milliliters",
    scale="1e-6",
    exponents={meters: 3},
    abbrev="mL",
    doc="""A milliliter is around 20 drops of water, or the size of a 1-cm cube."""
)
feet_cubed = make_compound_unit(
    scale=".02831685",
    exponents={feet: 3}
)
fluid_ounce = make_compound_unit(
    name="fluid ounce",
    exponents={meters: 3},  # As fl oz aren't defined in terms of some particular length cube
    scale="2.957353e-5",
    abbrev="fl oz",
)
fluid_ounce_imperial = make_compound_unit(
    name="imperial fluid ounce",
    exponents={meters: 3},
    scale="2.841306e-5",
)
cups = make_compound_unit(
    name="cups",
    exponents={meters: 3},
    scale="2.365882e-4",
    abbrev="c",
)
teaspoon = make_compound_unit(
    name="teaspoon",
    exponents={meters: 3},
    scale="4.928922e-6",
    abbrev="tsp",
)
tablespoon = make_compound_unit(
    name="tablespoon",
    exponents={meters: 3},
    scale="1.478676e-5",
    abbrev="tbsp"
)
gallon = make_compound_unit(
    name="gallon",
    exponents={meters: 3},
    scale="3.785412e-3",
    abbrev="gal"
)
imperial_gallon = make_compound_unit(
    name="imperial gallon",
    exponents={meters: 3},
    scale="4.54609e-3"
)
