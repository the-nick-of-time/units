from pyunitx.resistance import from_color, ohms


def test_simple_color():
    assert from_color("BKO") == ohms("10e3")


def test_capitalization():
    assert from_color("bko") == ohms("10e3")


def test_tolerance():
    assert from_color("eku", True) == (ohms("50e6"), ohms("10e6"))
    assert from_color("EKUL", True) == (ohms("50e6"), ohms("25e5"))
