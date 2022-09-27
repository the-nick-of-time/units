import pytest

from pyunitx.length import inches
from pyunitx.volume import feet_cubed, meters_cubed


def test_exponent_scale():
    cubic_inch = type(inches(4) ** 3)

    assert cubic_inch.scale == pytest.approx(feet_cubed.scale / (12 ** 3))


def test_automatic_converter():
    meters = meters_cubed("1e6")

    value = meters.to_kilometers_cubed()
    assert value == type(value)("1e-3")
