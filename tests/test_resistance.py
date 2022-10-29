from pyunitx.resistance import from_color, ohms


def test_simple_color():
    assert from_color("BKO") == ohms("10e3")


def test_capitalization():
    assert from_color("bko") == ohms("10e3")
