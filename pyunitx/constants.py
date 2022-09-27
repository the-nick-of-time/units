from decimal import Decimal

from pyunitx._api import make_compound_unit
from pyunitx.energy import joules
from pyunitx.length import meters
from pyunitx.mass import kilograms
from pyunitx.mole import mole
from pyunitx.power import watts
from pyunitx.pressure import pascals
from pyunitx.temperature import kelvin
from pyunitx.time import seconds
from pyunitx.velocity import meters_per_second

__all__ = [
    "c", "speed_of_light",
    "G", "gravitational_constant",
    "N_A", "avogadro",
    "σ", "stefan_boltzmann",
    "R", "gas_constant",
    "M_air", "air_molar_mass",
    "g", "earth_gravity",
    "atm", "standard_atmosphere",
    "R_E", "earth_radius",
    "M_E", "earth_mass",
]


# Most units from
# https://physics.nist.gov/cuu/Constants/Table/allascii.txt

def _construct_gravitational_constant():
    g_unit = make_compound_unit(scale=1, exponents={meters: 3, kilograms: -1, seconds: -2})
    return g_unit("6.67430e-11")


def _construct_stefan_boltzmann_constant():
    unit = make_compound_unit(scale=1, exponents={watts: 1, meters: -2, kelvin: -4})
    return unit("5.670374419e-8")


def _construct_standard_gravity():
    unit = make_compound_unit(scale=1, exponents={meters: 1, seconds: -2})
    return unit("9.80665")


def _construct_gas_constant():
    unit = make_compound_unit(scale=1, exponents={joules: 1, mole: -1, kelvin: -1})
    return unit("8.314462618")


def _construct_air_molar_mass():
    unit = make_compound_unit(scale=1, exponents={kilograms: 1, mole: -1})
    # https://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
    return unit(".0289647")


#: The speed of light in a vacuum *c* is an absolute constant of the universe.
#: It now forms the foundation for the definition of the meter.
#: It is given here in \frac{m}{s}.
c = speed_of_light = meters_per_second(299_792_458)

#: Newton's gravitational constant *G* shows up in the classical equation
#: :math:`F = \frac{GMm}{r^2}`.
#: It is given here in :math:`\frac{m^3}{kg s^2}`.
G = gravitational_constant = _construct_gravitational_constant()

#: Avogadro's number is the number of molecules making up one mole,
#: approximately :math:`6.022\times 10^{23}`
N_A = avogadro = Decimal("6.02214076e23")

#: The Stefan-Boltzmann constant relates the temperature of an object to how
#: much electromagnetic radiation it emits. It appears in the equation
#: :math:`j^* = \sigma T^4`.
#: It is given in units of :math:`\frac{W}{m^2 K^4}`.
σ = stefan_boltzmann = sigma = _construct_stefan_boltzmann_constant()

#: One standard atmosphere is approximately the average sea-level atmospheric
#: pressure.
atm = standard_atmosphere = pascals(101325)

#: The ideal gas constant relates the pressure, volume, quantity, and
#: temperature of a gas to each other.
#: This equation is :math:`PV = nRT`.
#: It is given in :math:`\frac{J}{mol K}`.
R = gas_constant = _construct_gas_constant()

#: The average molar mass of dry air means the mass of one mole of air.
#: Factoring in molar mass means you can transform the ideal gas law into
#: :math:`PV = \frac{m}{M_{air}} R T` if you have a mass instead of molarity
#: which is the common case.
#: It is in units of :math:`\frac{kg}{mol}`
M_air = air_molar_mass = _construct_air_molar_mass()

#: Standard earth's gravity is an average of measurements taken around the
#: world. If you live at a high elevation, you may measure a lower acceleration
#: because you are further from the center of the earth.
#: It is in units of :math:`\frac{m}{s^2}`
g = earth_gravity = _construct_standard_gravity()

#: The earth's equatorial radius, as measured for the WGS 84 ellipsoid.
#: Its value is retrieved from
#: `here <https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html>`_.
#: It is given in :math:`m`.
R_E = earth_radius = meters(6378137)

#: The earth's total mass. Its value is retrieved from
#: `here <https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html>`_.
#: It is given in :math:`kg`.
M_E = earth_mass = kilograms("5.9722e24")
