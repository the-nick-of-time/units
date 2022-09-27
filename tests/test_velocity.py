from units.length import meters, kilometers, feet, Length
from units.time import seconds, hours, minutes
from units.velocity import meters_per_second, kilometers_per_hour, miles_per_hour


def test_mph_to_kph():
    imperial = miles_per_hour(60)
    metric = kilometers_per_hour("96.56064")

    assert metric.sig_figs(3) == imperial.to_kilometers_per_hour().sig_figs(3)


def test_speed_for_time():
    v = kilometers_per_hour(80)
    t = hours(2)

    assert abs((kilometers(160) - (v * t)).value) < 0.0001
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
