from pyunitx._api import make_compound_dimension, make_compound_unit
from pyunitx.length import Length, meters

Area = make_compound_dimension(name="Area", exponents={Length: 2})

# no need to explain square meters
make_compound_unit(
    exponents={meters: 2},
    scale=1
)

make_compound_unit(
    name="acre",
    abbrev="acre",
    scale="4.046873e3",
    exponents={meters: 2},
    doc="""\
    An acre is a common measure of land area.
    """
)
make_compound_unit(
    name="hectare",
    abbrev="ha",
    scale="1e4",
    exponents={meters: 2},
    doc="""\
    A hectare is a unit of land area compatible with SI units, being defined as
    10,000 square meters or the area of a square 100 meters on a side.
    """
)
