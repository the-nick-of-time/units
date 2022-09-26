from units._api import make_dimension, make_unit

Quantity = make_dimension("Quantity")

mol = make_unit(name="mole", dimension=Quantity, scale=1)
