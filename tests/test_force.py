import pytest

from pyunitx import SIUNITX_OLD, OperationError
from pyunitx.constants import atm
from pyunitx.energy import joules
from pyunitx.force import pounds, kgf, newtons
from pyunitx.length import meters, kilometers
from pyunitx.pressure import bars


def test_equivalence():
    assert kgf(1).equivalent_to(pounds("2.205"), 3)


def test_complex_addition():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100)

    expected = newtons(1200100)
    assert (area * pressure).to_newtons() + extra_force == expected


def test_complex_subtraction():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100000)

    expected = newtons(1100000)
    assert (area * pressure).to_newtons() - extra_force == expected


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
    assert str(displacement * force) == "20 J"
    assert str(force / displacement) == "5 kg s^-2"


def test_complex_to_latex():
    displacement = meters(2)
    force = newtons(10)
    expected = joules(20)

    assert displacement.to_latex() == r"\qty{2}{m}"
    assert force.to_latex() == r"\qty{10}{N}"
    assert expected.to_latex() == r"\qty{20}{J}"
    assert (displacement * force).to_latex() == r"\qty{20}{J}"
    assert (force / displacement).to_latex() == r"\qty{5}{kg.s^{-2}}"


def test_complex_to_latex_old():
    displacement = meters(2)
    force = newtons(10)
    expected = joules(20)

    assert displacement.to_latex(SIUNITX_OLD) == r"\SI{2}{m}"
    assert force.to_latex(SIUNITX_OLD) == r"\SI{10}{N}"
    assert expected.to_latex(SIUNITX_OLD) == r"\SI{20}{J}"
    assert (displacement * force).to_latex(SIUNITX_OLD) == r"\SI{20}{J}"
    assert (force / displacement).to_latex(SIUNITX_OLD) == r"\SI{5}{kg.s^{-2}}"


def test_equal_identical():
    assert newtons(4) == newtons(2) * 2


def test_equal_incompatible():
    assert pounds(1) != newtons("4.4482216152605")


def test_equal_base_identical():
    km_in_m = meters(1000)
    km = kilometers(1)
    assert km == km_in_m.to_kilometers()


def test_equal_base_incompatible():
    km = kilometers(1)
    m = meters(1000)
    assert km != m


def test_add_base_identical():
    a = meters(1)
    b = meters(2)
    assert a + b == meters(3)


def test_add_base_incompatible():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(OperationError):
        print(a + b)


def test_subtract_base_identical():
    a = meters(5)
    b = meters(2)
    expected = meters(3)
    assert a - b == expected


def test_subtract_base_incompatible():
    a = meters(1)
    b = kilometers(1)
    with pytest.raises(OperationError):
        print(a - b)
