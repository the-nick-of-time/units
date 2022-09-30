from pyunitx.frequency import hertz, kilohertz
from pyunitx.length import kilometers, feet, meters
from pyunitx.time import seconds, hours, minutes, milliseconds


def test_hertz_cancel():
    freq = hertz(440)
    duration = seconds(".5")

    assert freq * duration == 220


def test_name():
    assert type(kilometers(1) / hours(1)).__name__ == "kilometers_per_hour"


def test_scaled_divisions():
    d = feet("393.7")
    t = minutes(2)

    assert (d / t).equivalent_to(meters(1) / seconds(1), 2)


def test_rdiv():
    t = milliseconds(2)

    assert (4 / t).to_kilohertz() == kilohertz(2)
