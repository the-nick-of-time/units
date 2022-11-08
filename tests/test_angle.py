import math
from decimal import Decimal

import pytest

from pyunitx.angle import degree


def test_to_radian():
    assert degree(57.2957795).to_radians() == pytest.approx(1)
    assert degree(180).to_radians() == pytest.approx(Decimal(math.pi))


def test_from_radian():
    assert degree.from_radians(math.pi).sig_figs(3) == degree(180)
    assert degree.from_radians(1).sig_figs(3) == degree("57.3")
