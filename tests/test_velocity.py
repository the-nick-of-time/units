import pytest

from units.length import meters, kilometers, feet, Length
from units.time import seconds, hours, minutes
from units.velocity import meters_per_second, kilometers_per_hour, miles_per_hour


def patch_factory(unit, name):
    def abs_(self):
        return type(self)(abs(self.value))

    def le(self, other):
        return (self.composition == other.composition
                and self.value * self.scale <= other.value * other.scale)

    @pytest.fixture(name=name)
    def patcher(monkeypatch):
        monkeypatch.setattr(unit, "__abs__", abs_, raising=False)
        monkeypatch.setattr(unit, "__le__", le, raising=False)

    globals()[name] = patcher
    return patcher


patch_factory(kilometers_per_hour, "kph_approx")
patch_factory(kilometers, "km_approx")


def quantities_approx_equal(expected, actual, tol=1e-6):
    return abs(expected - actual) <= type(expected)(tol)


# noinspection PyUnusedLocal
def test_mph_to_kph(kph_approx):
    imperial = miles_per_hour(60)
    metric = kilometers_per_hour("96.56064")

    assert quantities_approx_equal(metric, imperial.to_kilometers_per_hour())


# noinspection PyUnusedLocal
def test_speed_for_time(km_approx):
    v = kilometers_per_hour(80)
    t = hours(2)

    assert quantities_approx_equal(kilometers(160), v * t)
    assert (v * t).is_dimension(Length)


def test_distance_over_time():
    d = meters(10)
    t = seconds(2)
    v = meters_per_second(5)

    assert (d / t) == v


def test_name():
    assert kilometers_per_hour.__name__ == "kilometers_per_hour"


def test_scaled_divisions():
    d = feet("393.7")
    t = minutes(2)
    v = meters_per_second(1)

    assert (d / t).equivalent_to(v, within=0.0001)
