from decimal import Decimal

from units.base import make_compound_dimension, make_compound_unit
from units.length import Length, meters
from units.mass import Mass, kilograms
from units.power import Power, watts
from units.pressure import pascals
from units.temperature import Temperature, kelvin
from units.time import Time, seconds
from units.velocity import meters_per_second


# Most units from
# https://physics.nist.gov/cuu/Constants/Table/allascii.txt

def _construct_gravitational_constant():
    g_dimension = make_compound_dimension(((Length, 3), (Mass, -1), (Time, -2)))
    g_unit = make_compound_unit(g_dimension, 1, ((meters, 3), (kilograms, -1), (seconds, -2)))
    return g_unit("6.67430e-11")


def _construct_stefan_boltzmann_constant():
    dim = make_compound_dimension(((Power, 1), (Length, -2), (Temperature, -4)))
    unit = make_compound_unit(dim, 1, ((watts, 1), (meters, -2), (kelvin, -4)))
    return unit("5.670374419e-8")


def _construct_standard_gravity():
    dim = make_compound_dimension({Length: 1, Time: -2})
    unit = make_compound_unit(dim, 1, {meters: 1, seconds: -2})
    return unit("9.80665")


c = speed_of_light = meters_per_second(299_792_458)
G = gravity = _construct_gravitational_constant()
N_A = avogadro = Decimal("6.02214076e23")
σ = stefan_boltzmann = sigma = _construct_stefan_boltzmann_constant()
atm = standard_atmosphere = pascals(101325)
g = earth_gravity = _construct_standard_gravity()
