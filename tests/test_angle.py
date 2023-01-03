import math
from decimal import Decimal

import pytest

from pyunitx.angle import degrees
from pyunitx.time import seconds


def test_to_radian():
    assert degrees(57.2957795).to_radians() == pytest.approx(1)
    assert degrees(180).to_radians() == pytest.approx(Decimal(math.pi))


def test_from_radian():
    assert degrees.from_radians(math.pi).sig_figs(3) == degrees(180)
    assert degrees.from_radians(1).sig_figs(3) == degrees("57.3")


def test_from_dms():
    assert degrees.from_dms(1, 30, 36) == degrees("1.51")
    assert degrees.from_dms((1, 30, 36)) == degrees("1.51")
    assert degrees.from_dms([1, 30, 36]) == degrees("1.51")


def test_from_decimal_string():
    assert degrees.from_dms("1.23 ") == degrees("1.23")
    assert degrees.from_dms("1.23°") == degrees("1.23")
    assert degrees.from_dms("-1.23°") == degrees("-1.23")


def test_from_dms_string():
    assert degrees.from_dms("1°30'36\"") == degrees("1.51")
    assert degrees.from_dms("1°30′36″") == degrees("1.51")
    assert degrees.from_dms("1°30′36.36″") == degrees("1.5101")
    assert degrees.from_dms("1° 30′ 36″  ") == degrees("1.51")


def test_from_dms_fail():
    with pytest.raises(ValueError):
        degrees.from_dms("foobar")
    with pytest.raises(ValueError):
        degrees.from_dms("123deg")


def test_compound_to_radians():
    speed = degrees(90) / seconds(1)

    assert speed.to_radians_per_second().equivalent_to(math.pi / 2 / seconds(1))
