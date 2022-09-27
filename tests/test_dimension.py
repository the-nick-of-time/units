from pyunitx._api import DimensionBase


def test_base_create():
    a = DimensionBase('a', ())

    assert a.__name__ == 'a'
    assert a.composition.to_pairs() == ((a, 1),)


def test_flyweight_bases():
    a = DimensionBase('a', ())
    alias = DimensionBase('a', ())
    b = DimensionBase('b', ())

    assert a is alias
    assert a is not b


def test_flyweight_post_base():
    a = DimensionBase('a', ())
    b = DimensionBase('b', ())
    alias = DimensionBase('a', ((a, 1),))

    assert a is alias
    assert a is not b


def test_flyweight_complex():
    a = DimensionBase('a', ())
    b = DimensionBase('b', ())
    complex = DimensionBase('c', ((a, 1), (b, -2)))
    doubled = DimensionBase('d', ((a, 2), (b, -4)))
    alias = DimensionBase('alias', ((complex, 2),))

    assert alias is doubled


def test_flyweight_one_complex():
    a = DimensionBase('a', ())
    b = DimensionBase('b', ())
    complex = DimensionBase('c', ((a, 1), (b, -2)))
    alias = DimensionBase('alias', ((complex, 1),))

    assert alias is complex


def test_zero_exponent():
    a = DimensionBase('a', ())
    b = DimensionBase('b', ())
    complex = DimensionBase('c', ((a, 2), (b, 0)))
    alias = DimensionBase('alias', ((a, 2),))

    assert complex is alias
