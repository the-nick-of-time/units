from pyunitx.constants import g, R_E, M_E, G


def test_gravity_derivation():
    a = G * M_E / (R_E ** 2)

    assert a.equivalent_to(g, 0.1)
