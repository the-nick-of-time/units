from units._api import make_compound_dimension, make_compound_unit
from units.force import Force, pounds, newtons
from units.length import Length, meters, inches

__all__ = ["Pressure", "pascals", "bars", "psi"]

Pressure = make_compound_dimension({Force: 1, Length: -2})

pascals = make_compound_unit(
    scale=1,
    exponents={newtons: 1, meters: -2},
    name="pascals",
    doc="""The pascal is the base unit of pressure, but it is very small."""
)
bars = make_compound_unit(
    scale=1e5,
    exponents={newtons: 1, meters: -2},
    name="bars",
    doc=r"""\
    A bar is 10\ :sup:`5` pascals, around sea level atmospheric pressure.
    """
)
psi = make_compound_unit(
    scale="6.894757e3",
    exponents={pounds: 1, inches: -2},
    name="psi",
    doc="""\
    Pounds per square inch are the typical units of pressure in |ucs|, despite 
    not using the base unit of length.
    """
)
