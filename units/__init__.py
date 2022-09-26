"""A module for the programming-level manipulation of physical quantities.

Most conversion factors come from this document: https://physics.nist.gov/cuu/pdf/sp811.pdf
And most values of constants come from this one:
https://physics.nist.gov/cuu/Constants/Table/allascii.txt
"""

# Importing all defined dimensions will ensure that all conversion functions
# will work. Otherwise, the first time a calculation generates a unit, it will
# create a new dimension that doesn't know about any of the other units
# available.
# noinspection PyUnresolvedReferences
from . import (
    _api,
    angle,
    constants,
    derived,
    energy,
    force,
    length,
    mass,
    mole,
    power,
    pressure,
    temperature,
    time,
    velocity,
    volume,
)
