from pyunitx.constants import g, R_E, M_E, G, R
from pyunitx.force import pounds
from pyunitx.mass import pounds_mass


def test_gravity_derivation():
    a = G * M_E / (R_E ** 2)

    assert a.equivalent_to(g, 2)


def test_pound_mass():
    assert (g.to_feet_per_second_squared() * pounds_mass(1)).equivalent_to(pounds(1), 5)


def test_gas_constant_to_usc():
    us = R.to_feet_pounds_per_mole_per_rankine()

    assert us.sig_figs(4) == type(us)("3.407")
