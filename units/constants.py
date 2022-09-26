from decimal import Decimal

from units.base import make_compound_unit
from units.energy import joules
from units.length import meters
from units.mass import kilograms
from units.mole import mol
from units.power import watts
from units.pressure import pascals
from units.temperature import kelvin
from units.time import seconds
from units.velocity import meters_per_second

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
    unit = make_compound_unit(scale=1, exponents={joules: 1, mol: -1, kelvin: -1})
    return unit("8.314462618")


def _construct_air_molar_mass():
    unit = make_compound_unit(scale=1, exponents={kilograms: 1, mol: -1})
    # https://www.engineeringtoolbox.com/molecular-mass-air-d_679.html
    return unit(".0289647")


c = speed_of_light = meters_per_second(299_792_458)
G = gravitational_constant = _construct_gravitational_constant()
N_A = avogadro = Decimal("6.02214076e23")
σ = stefan_boltzmann = sigma = _construct_stefan_boltzmann_constant()
atm = standard_atmosphere = pascals(101325)
R = gas_constant = _construct_gas_constant()
M_air = air_molar_mass = _construct_air_molar_mass()
g = earth_gravity = _construct_standard_gravity()
# https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
# Actually the equatorial radius/semimajor axis of the WGS 84 ellipsoid
R_E = earth_radius = meters(6378137)
M_E = earth_mass = kilograms("5.9722e24")
