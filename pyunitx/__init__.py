"""A module for the first-class manipulation of physical quantities.

It is named ``pyunitx`` as a reference to the ``siunitx`` LaTeX package.

Most conversion factors come from
`this document from NIST <https://physics.nist.gov/cuu/pdf/sp811.pdf>`_.
Most values of constants come from
`this list also from NIST <https://physics.nist.gov/cuu/Constants/Table/allascii.txt>`_.
"""

from . import (
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
# Importing all defined dimensions will ensure that all conversion functions
# will work. Otherwise, the first time a calculation generates a unit, it will
# create a new dimension that doesn't know about any of the other units
# available.
# noinspection PyUnresolvedReferences
from ._api import (
    make_dimension,
    make_unit,
    make_compound_dimension,
    make_compound_unit,
    SIUNITX_OLD,
    SIUNITX_NEW,
)
