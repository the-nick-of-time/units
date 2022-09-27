from units._api import make_compound_dimension, make_compound_unit
from units.energy import Energy, joules
from units.force import pounds
from units.length import feet
from units.time import Time, seconds

__all__ = ["Power", "watts", "horsepower"]

Power = make_compound_dimension({Energy: 1, Time: -1})

watts = make_compound_unit(
    scale=1,
    exponents={joules: 1, seconds: -1},
    name="watts",
    abbrev="W",
    doc="""\
    A watt is a joule per second. In most cases, like calculating the energy
    expenditure of a heating system, collecting rates of energy use is the most
    useful then multiplying by time to get overall energy usage.
    """
)
horsepower = make_compound_unit(
    scale="7.456999e2",
    exponents={feet: 1, pounds: 1, seconds: -1},
    abbrev="hp",
    doc="""
    One horsepower is 550 foot-pounds per second, and is produced by a very 
    standards-compliant equine.
    """
)
