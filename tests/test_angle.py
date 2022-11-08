import math
from decimal import Decimal

import pytest

from pyunitx.angle import degrees


def test_to_radian():
    assert degrees(57.2957795).to_radians() == pytest.approx(1)
    assert degrees(180).to_radians() == pytest.approx(Decimal(math.pi))


def test_from_radian():
    assert degrees.from_radians(math.pi).sig_figs(3) == degrees(180)
    assert degrees.from_radians(1).sig_figs(3) == degrees("57.3")
