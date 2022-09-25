from units.base import make_compound_unit, make_compound_dimension
from units.force import Force, pounds, newtons
from units.length import Length, meters, inches

__all__ = ["Pressure", "pascals", "bars", "psi"]

Pressure = make_compound_dimension({Force: 1, Length: -2})

pascals = make_compound_unit(1, {newtons: 1, meters: -2}, name="pascals")
bars = make_compound_unit(1e5, {newtons: 1, meters: -2}, name="bars")
psi = make_compound_unit("6.894757e3", {pounds: 1, inches: -2}, name="psi")
