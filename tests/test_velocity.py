from units.length import meters, kilometers
from units.time import seconds, hours
from units.velocity import meters_per_second, kilometers_per_hour, miles_per_hour


def test_mph_to_kph():
    imperial = miles_per_hour(60)
    metric = kilometers_per_hour(96.56)

    assert imperial.to_KilometersPerHour() == metric


def test_speed_for_time():
    v = kilometers_per_hour(80)
    t = hours(2)

    assert v * t == kilometers(160)


def test_distance_over_time():
    d = meters(10)
    t = seconds(2)
    v = meters_per_second(5)

    assert (d / t) == v
