import pytest

from units.base import make_dimension, make_unit, Multiset, Compound


@pytest.fixture
def first_dimension():
    return make_dimension("TEST1")


@pytest.fixture
def second_dimension():
    return make_dimension("TEST2")


@pytest.fixture
def unit_1a(first_dimension):
    return make_unit(name="unit_1a", dimension=first_dimension, scale=1)


@pytest.fixture
def unit_1b(first_dimension):
    return make_unit(name="unit_1b", dimension=first_dimension, scale=10)


@pytest.fixture
def unit_2(second_dimension):
    return make_unit(name="unit_2", dimension=second_dimension, scale=1)


def test_creation(unit_1a, unit_2):
    compound = Compound(((unit_1a, 1), (unit_2, -1)))

    assert {unit_1a: 1, unit_2: -1} == compound.units.store


def test_equality(unit_1a, unit_2):
    a = Compound(((unit_1a, 1), (unit_2, -1)))
    b = Compound(((unit_1a, 1), (unit_2, -1)))

    assert a == b


def test_multiply(unit_1a, unit_2):
    a = Compound(((unit_1a, 1), (unit_2, -1)))
    b = Compound(((unit_1a, 1), (unit_2, 2)))

    result = a * b

    assert Compound(((unit_1a, 1), (unit_2, -1))) == a
    assert Compound(((unit_1a, 2), (unit_2, 1))) == result


def test_divide(unit_1a, unit_2):
    a = Compound(((unit_1a, 1), (unit_2, -1)))
    b = Compound(((unit_1a, 1), (unit_2, 2)))

    result = a / b

    assert Compound(((unit_1a, 1), (unit_2, -1))) == a
    assert Compound(((unit_2, -3),)) == result


def test_creation_pairs(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    multiset = Multiset(pairs)

    assert {unit_1a: 1, unit_1b: -1} == multiset.store


def test_creation_copy(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    source = Multiset(pairs)
    dest = Multiset(source)

    assert source == dest


def test_multiset_equality(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    a = Multiset(pairs)
    b = Multiset(pairs)

    assert a == b


def test_add(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    source = Multiset(pairs)
    added = source.add(unit_1a)

    assert {unit_1a: 2, unit_1b: -1} == added.store


def test_add_zero(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    source = Multiset(pairs)
    added = source.add(unit_1b)

    assert {unit_1a: 1} == added.store


def test_add_compound(unit_1a, unit_1b):
    a = Multiset(((unit_1a, 1), (unit_1b, -1)))
    b = Multiset(((unit_1a, -1), (unit_1b, -1)))

    added = a.add(b)

    assert {unit_1b: -2} == added.store


def test_remove(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    source = Multiset(pairs)
    subtracted = source.remove(unit_1b)

    assert {unit_1a: 1, unit_1b: -2} == subtracted.store


def test_remove_zero(unit_1a, unit_1b):
    pairs = ((unit_1a, 1), (unit_1b, -1))

    source = Multiset(pairs)
    subtracted = source.remove(unit_1a)

    assert {unit_1b: -1} == subtracted.store


def test_remove_compound(unit_1a, unit_1b):
    a = Multiset(((unit_1a, 1), (unit_1b, -1)))
    b = Multiset(((unit_1a, -1), (unit_1b, -1)))

    subtracted = a.remove(b)

    assert {unit_1a: 2} == subtracted.store
