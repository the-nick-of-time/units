from units.base import make_dimension, make_unit

Quantity = make_dimension("Quantity")

mol = make_unit("mole", Quantity, 1)
