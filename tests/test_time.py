from pyunitx.time import seconds, hertz


def test_hertz_cancel():
    freq = hertz(440)
    duration = seconds(".5")

    assert freq * duration == 220
