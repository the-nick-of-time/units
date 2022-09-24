import pytest

from units.length import meters, kilometers
from units.time import seconds, hours
from units.velocity import meters_per_second, kilometers_per_hour, miles_per_hour

abs_ = lambda self: type(self)(abs(self.value))
le = lambda self, other: self.composition == other.composition and self.value <= other.value


@pytest.fixture
def kph_approx(monkeypatch):
    monkeypatch.setattr(kilometers_per_hour, "__abs__", abs_, raising=False)
    monkeypatch.setattr(kilometers_per_hour, "__le__", le, raising=False)


@pytest.fixture
def km_approx(monkeypatch):
    monkeypatch.setattr(kilometers, "__abs__", abs_, raising=False)
    monkeypatch.setattr(kilometers, "__le__", le, raising=False)


def quantities_approx_equal(expected, actual, tol=1e-6):
    return abs(expected - actual) <= type(expected)(tol)


# noinspection PyUnusedLocal
def test_mph_to_kph(kph_approx):
    imperial = miles_per_hour(60)
    metric = kilometers_per_hour("96.56064")

    assert quantities_approx_equal(metric, imperial.to_KilometersPerHour())


# noinspection PyUnusedLocal
def test_speed_for_time(km_approx):
    v = kilometers_per_hour(80)
    t = hours(2)

    assert quantities_approx_equal(kilometers(160), v * t)


def test_distance_over_time():
    d = meters(10)
    t = seconds(2)
    v = meters_per_second(5)

    assert (d / t) == v
