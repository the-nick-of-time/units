from pyunitx._api import make_dimension, make_unit, si_unit

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
generated = si_unit(
    base_unit=mole,
    short_doc="SI prefixes are useful for very large or small quantities.",
)
globals().update(generated)

__all__ = [
              "Quantity",
              "mole",
          ] + list(generated.keys())
