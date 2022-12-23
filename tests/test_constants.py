from fractions import Fraction
from math import pi

from pyunitx.constants import g, R_E, M_E, G, R, c
from pyunitx.force import pounds
from pyunitx.frequency import gigahertz
from pyunitx.length import meters, kilometers
from pyunitx.mass import pounds_mass
from pyunitx.time import sidereal_days


def test_gravity_derivation():
    a = G * M_E / (R_E ** 2)

    assert a.equivalent_to(g, 2)


def test_pound_mass():
    assert (g.to_feet_per_second_squared() * pounds_mass(1)).equivalent_to(pounds(1), 5)


def test_gas_constant_to_usc():
    us = R.to_feet_pounds_per_mole_per_rankine()

    assert us.sig_figs(4) == type(us)("3.407")


def test_light_frequency():
    assert (c / gigahertz(1)).to_meters() == meters("0.299792458")


def test_geosync_radius():
    r = (G * M_E * (sidereal_days(1).to_seconds() / (2 * pi)) ** 2) ** Fraction(1, 3)

    assert r.sig_figs(5) == (kilometers(35786).to_meters() + R_E).sig_figs(5)
