import pytest

from pyunitx.resistance import from_color, ohms
from pyunitx.temperature import kelvin


def test_simple_color():
    assert from_color("BKO") == ohms("10e3")


def test_capitalization():
    assert from_color("bko") == ohms("10e3")


def test_tolerance():
    assert from_color("eku", True) == (ohms("50e6"), ohms("10e6"))
    assert from_color("EKUL", True) == (ohms("50e6"), ohms("25e5"))
    assert from_color("EOVUS", True) == (ohms("537e6"), ohms("537e5"))


def test_sensitivity():
    assert from_color("REEOBU", include_coeff=True) == (ohms("255e3"),
                                                        ohms("2.55e3"),
                                                        ohms("255e-2") / kelvin(1))


def test_default_sensitivity():
    with pytest.raises(KeyError):
        from_color("BKO", include_coeff=True)


def test_bounds():
    with pytest.raises(ValueError):
        from_color("BK")
    with pytest.raises(ValueError):
        from_color("REEOBUL")
