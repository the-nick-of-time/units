from pyunitx.constants import g, R_E, M_E, G, R
from pyunitx.force import pounds
from pyunitx.mass import av_pound


def test_gravity_derivation():
    a = G * M_E / (R_E ** 2)

    assert a.equivalent_to(g, 0.1)


def test_pound_mass():
    assert (g.to_feet_per_second_squared() * av_pound(1)).equivalent_to(pounds(1), .001)


def gas_constant_to_usc():
    us = R.to_feet_pounds_per_rankine_per_slug()

    assert us.sig_figs(4) == type(us)("49.72")
