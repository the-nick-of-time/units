import enum
from decimal import Decimal

from pyunitx._api import make_compound_unit, make_compound_dimension, si_unit
from pyunitx.current import Current, amperes
from pyunitx.voltage import Potential, volts

Resistance = make_compound_dimension(name="Resistance", exponents={Potential: 1, Current: -1})

ohms = make_compound_unit(
    name="ohms",
    abbrev="Ω",
    exponents={volts: 1, amperes: -1},
    scale=1,
    doc="""\
    A current of one ampere traveling through one ohm of resistance drops its
    potential by one volt.
    """
)

generated = si_unit(base_unit=ohms)
globals().update(generated)


class Color(enum.Enum):
    BLACK = "K"
    BROWN = "B"
    RED = "R"
    ORANGE = "O"
    YELLOW = "Y"
    GREEN = "E"
    BLUE = "U"
    VIOLET = "V"
    GRAY = "G"
    WHITE = "W"
    GOLD = "L"
    SILVER = "S"
    BLANK = None

    def digit(self):
        values = {
            Color.BLACK: 0,
            Color.BROWN: 1,
            Color.RED: 2,
            Color.ORANGE: 3,
            Color.YELLOW: 4,
            Color.GREEN: 5,
            Color.BLUE: 6,
            Color.VIOLET: 7,
            Color.GRAY: 8,
            Color.WHITE: 9,
        }
        return values[self]

    def multiplier(self):
        multipliers = {
            Color.BLACK: 10 ** 0,
            Color.BROWN: 10 ** 1,
            Color.RED: 10 ** 2,
            Color.ORANGE: 10 ** 3,
            Color.YELLOW: 10 ** 4,
            Color.GREEN: 10 ** 5,
            Color.BLUE: 10 ** 6,
            Color.VIOLET: 10 ** 7,
            Color.GRAY: 10 ** 8,
            Color.WHITE: 10 ** 9,
            Color.GOLD: 10 ** -1,
            Color.SILVER: 10 ** -2,
        }
        return multipliers[self]

    def tolerance(self):
        tolerances = {
            Color.BROWN: Decimal(1),
            Color.RED: Decimal(2),
            Color.GREEN: Decimal(".5"),
            Color.BLUE: Decimal(".25"),
            Color.VIOLET: Decimal(".1"),
            Color.GRAY: Decimal(".05"),
            Color.GOLD: Decimal("5"),
            Color.SILVER: Decimal("10"),
            Color.BLANK: Decimal("20"),
        }
        return tolerances[self] / 100


def from_color(spec: str, include_tol=False) -> ohms:
    spec = spec.upper()
    if len(spec) == 4:
        digits = spec[:2]
        multiplier = spec[2]
        tolerance = spec[3]
        sensitivity = None
    elif len(spec) == 5:
        digits = spec[:3]
        multiplier = spec[3]
        tolerance = spec[4]
        sensitivity = None
    elif len(spec) == 6:
        digits = spec[:3]
        multiplier = spec[3]
        tolerance = spec[4]
        sensitivity = spec[5]
    elif len(spec) == 3:
        digits = spec[:2]
        multiplier = spec[2]
        tolerance = None
        sensitivity = None
    else:
        raise ValueError("Resistor codes can be 3-6 bands long.")
    value = 0
    for i, char in enumerate(digits[::-1]):
        e = Color(char)
        value += e.digit() * 10 ** i
    value *= Color(multiplier).multiplier()
    if include_tol:
        return ohms(value), ohms(value) * Color(tolerance).tolerance()
    return ohms(value)


__all__ = [
    "Resistance",
    "ohms",
    "from_color",
    "Color",
    *generated.keys()
]
