from pyunitx._api import make_dimension, make_unit

Charge = make_dimension("Charge")

coulombs = make_unit(
    name="coulombs",
    abbrev="C",
    dimension=Charge,
    scale=1,
    doc="""\
    A coulomb is formally defined as the amount of charge that travels past a
    point in a 1-Ampere current over the course of one second. Current is the
    defined fundamental quantity in the SI system, and is certainly easier to
    measure directly, but charge cannot be decomposed.
    """
)
fundamental_charge = make_unit(
    name="fundamental_charge",
    abbrev="e",
    dimension=Charge,
    scale="1.602176634e-19",
    doc="""\
    This is the charge of a single proton or electron.
    """
)
