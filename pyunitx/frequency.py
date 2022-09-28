from pyunitx._api import make_compound_dimension, make_compound_unit
from pyunitx.time import Time, seconds, minutes

Frequency = make_compound_dimension({Time: -1}, "Frequency")
hertz = make_compound_unit(
    name="hertz",
    scale=1,
    exponents={seconds: -1},
    abbrev="Hz",
    doc="""\
    The hertz represents an occurrence once per second. Most commonly,
    this is used to measure sounds, where the occurrence is a soundwave peak 
    passing. 
    """
)
rpm = make_compound_unit(
    name="rpm",
    scale=1 / 60,
    exponents={minutes: -1},
    abbrev="rpm",
    doc="""\
    Revolutions per minute measure the action of a piston crank or of a wheel.
    """
)