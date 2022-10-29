import enum

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


def from_color(spec: str) -> ohms:
    value = 0
    spec = spec.upper()
    for i, char in enumerate(spec[-2::-1]):
        e = Color(char)
        value += e.digit() * 10 ** i
    value *= Color(spec[-1]).multiplier()
    return ohms(value)


__all__ = [
    "Resistance",
    "ohms",
    "from_color",
    "Color",
    *generated.keys()
]
