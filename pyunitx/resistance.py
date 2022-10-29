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

    def digit(self):
        values = {
            "K": 0,
            "B": 1,
            "R": 2,
            "O": 3,
            "Y": 4,
            "E": 5,
            "U": 6,
            "V": 7,
            "G": 8,
            "W": 9,
        }
        return values[self.value]

    def multiplier(self):
        multipliers = {
            "K": 10 ** 0,
            "B": 10 ** 1,
            "R": 10 ** 2,
            "O": 10 ** 3,
            "Y": 10 ** 4,
            "G": 10 ** 5,
            "U": 10 ** 6,
            "V": 10 ** 7,
        }
        return multipliers[self.value]


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
