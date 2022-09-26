from units._api import make_compound_dimension, make_compound_unit
from units.length import Length, meters

Volume = make_compound_dimension({Length: 3}, "Volume")

cubic_meter = make_compound_unit(scale=1, exponents={meters: 3})
liter = make_compound_unit(scale="1e-3", exponents={meters: 3})
milliliter = make_compound_unit(scale="1e-6", exponents={meters: 3})
