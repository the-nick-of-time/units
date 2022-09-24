from units.base import make_compound_dimension, make_compound_unit
from units.energy import Energy, joules
from units.force import pounds
from units.length import feet
from units.time import Time, seconds

__all__ = ["Power", "watts", "horsepower"]

Power = make_compound_dimension({Energy: 1, Time: -1})

watts = make_compound_unit(Power, 1, {joules: 1, seconds: -1}, "watts")
horsepower = make_compound_unit(Power, "7.456999e2", {feet: 1, pounds: 1, seconds: -1})
