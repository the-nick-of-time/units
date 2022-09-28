from pyunitx._api import make_compound_unit, make_compound_dimension
from pyunitx.current import Current, amperes
from pyunitx.voltage import Potential, volts

Resistance = make_compound_dimension(name="Resistance", exponents={Potential: 1, Current: -1})

ohm = make_compound_unit(
    name="ohm",
    abbrev="Ω",
    exponents={volts: 1, amperes: -1},
    scale=1,
    doc="""\
    A current of one ampere traveling through one ohm of resistance drops its
    potential by one volt.
    """
)
