import pytest

from pyunitx.length import inches
from pyunitx.volume import feet_cubed


def test_exponent_scale():
    cubic_inch = type(inches(4) ** 3)

    assert cubic_inch.scale == pytest.approx(feet_cubed.scale / (12 ** 3))
