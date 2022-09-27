from pyunitx._api import make_dimension, make_unit

__all__ = [
    "Quantity",
    "mole",
]

Quantity = make_dimension("Quantity")

mole = make_unit(
    name="mole",
    dimension=Quantity,
    scale=1,
    abbrev="mol",
    doc="""\
    A mole is the number of atoms in 12 grams of carbon-12.
    
    It basically is a dimensionless quantity, but is included in the SI system
    for its pragmatic usefulness in chemistry and fluid physics.
    """
)
