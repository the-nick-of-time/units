import pytest

from pyunitx._api import Multiset
from pyunitx.length import meters
from pyunitx.time import seconds


@pytest.fixture
def speed():
    return Multiset({meters: 1, seconds: -1})


def test_from_pairs():
    m = Multiset(((meters, 1), (seconds, -1)))

    assert m.store == {meters: 1, seconds: -1}


def test_from_dict():
    d = {meters: 1, seconds: -1}
    m = Multiset(d)

    assert m.store == d
    assert m.store is not d


def test_from_dict_with_zero():
    m = Multiset({meters: 1, seconds: 0})

    assert m.store == {meters: 1}


def test_from_other(speed):
    copy = Multiset(speed)

    assert copy.store == speed.store
    assert copy.store is not speed.store


def test_iter(speed):
    assert list(speed) == [meters, seconds]


def test_getitem(speed):
    assert speed[seconds] == -1


def test_eq_same(speed):
    copy = Multiset({seconds: -1, meters: 1})

    assert speed == copy
    assert speed != copy.remove(seconds)


def test_eq_wrong_type(speed):
    assert speed != {meters: 1, seconds: -1}


def test_str():
    m = Multiset({seconds: -2, meters: 3})

    assert str(m) == "meters_cubed_per_second_squared"


def test_add_immutable(speed):
    new = speed.add(seconds)

    assert new is not speed
    assert new.store == {meters: 1}
    assert speed.store == {meters: 1, seconds: -1}


def test_remove_immutable(speed):
    new = speed.remove(seconds)

    assert new is not speed
    assert new.store == {meters: 1, seconds: -2}
    assert speed.store == {meters: 1, seconds: -1}


def test_pairs(speed):
    assert speed.to_pairs() == ((meters, 1), (seconds, -1))
    m = Multiset({seconds: -1, meters: 1})
    assert m.to_pairs() == ((meters, 1), (seconds, -1))
