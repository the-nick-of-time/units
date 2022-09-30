from pyunitx._api import make_compound_unit, make_compound_dimension, si_unit
from pyunitx.charge import Charge, coulombs
from pyunitx.time import Time, seconds



Current = make_compound_dimension(name="Current", exponents={Charge: 1, Time: -1})

amperes = make_compound_unit(
    name="amperes",
    abbrev="A",
    scale=1,
    exponents={coulombs: 1, seconds: -1},
    doc="""\
    An ampere is a rate of charge movement equal to one coulomb per second.
    """
)

generated = si_unit(base_unit=amperes, short_doc="The :class:`ampere` is the SI base unit.")

__all__ = [
              "Current",
              "amperes",
          ] + list(generated.keys())
