import pytest

from pyunitx.constants import atm
from pyunitx.energy import joules
from pyunitx.force import pounds, kgf, newtons
from pyunitx.length import meters
from pyunitx.pressure import bars


def test_equivalence():
    assert kgf(1).equivalent_to(pounds(2.2), .05)


def test_complex_addition():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100)

    expected = newtons(1200100)
    assert area * pressure + extra_force == expected


def test_complex_subtraction():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100000)

    expected = newtons(1100000)
    assert area * pressure - extra_force == expected


def test_work():
    displacement = meters(2)
    force = newtons(10)
    expected = joules(20)

    assert displacement * force == expected


def test_sig_figs():
    area = meters(2) ** 2
    pressure = atm
    rounded = newtons(405000)  # exact is 405300

    assert (area * pressure).sig_figs(3) == rounded


def test_component_cannot_sqrt():
    f = joules(100)
    with pytest.raises(ValueError):
        print(f ** (1 / 2))


def test_complex_tostring():
    displacement = meters(2)
    force = newtons(10)
    expected = joules(20)

    assert str(displacement) == "2 m"
    assert str(force) == "10 N"
    assert str(expected) == "20 J"
    assert str(displacement * force) == "20 m^2 kg s^-2"
