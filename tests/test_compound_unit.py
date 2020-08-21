from unittest import TestCase

from base import make_dimension, make_unit
from extras import Multiset, CompoundUnit


class TestCompoundUnit(TestCase):
    def setUp(self):
        self.first_dimension = make_dimension("TEST1")
        self.second_dimension = make_dimension("TEST2")
        self.unit_1a = make_unit("unit_1a", self.first_dimension, 1)
        self.unit_1b = make_unit("unit_1b", self.first_dimension, 10)
        self.unit_2 = make_unit("unit_2", self.second_dimension, 1)

    def test_creation(self):
        compound = CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1)))

        self.assertEqual({self.unit_1a: 1, self.unit_2: -1}, compound.units.store)

    def test_equality(self):
        a = CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1)))
        b = CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1)))

        self.assertEqual(a, b)

    def test_multiply(self):
        a = CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1)))
        b = CompoundUnit(((self.unit_1a, 1), (self.unit_2, 2)))

        result = a * b

        self.assertEqual(CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1))), a)
        self.assertEqual(CompoundUnit(((self.unit_1a, 2), (self.unit_2, 1))), result)

    def test_divide(self):
        a = CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1)))
        b = CompoundUnit(((self.unit_1a, 1), (self.unit_2, 2)))

        result = a / b

        self.assertEqual(CompoundUnit(((self.unit_1a, 1), (self.unit_2, -1))), a)
        self.assertEqual(CompoundUnit(((self.unit_2, -3),)), result)


class TestMultiSet(TestCase):
    def setUp(self):
        self.dimension = make_dimension("TEST")
        self.first = make_unit("first", self.dimension, 1)
        self.second = make_unit("second", self.dimension, 10)

    def test_creation_pairs(self):
        pairs = ((self.first, 1), (self.second, -1))

        multiset = Multiset(pairs)

        self.assertEqual({self.first: 1, self.second: -1}, multiset.store)

    def test_creation_copy(self):
        pairs = ((self.first, 1), (self.second, -1))

        source = Multiset(pairs)
        dest = Multiset(source)

        self.assertEqual(source, dest)

    def test_equality(self):
        pairs = ((self.first, 1), (self.second, -1))

        a = Multiset(pairs)
        b = Multiset(pairs)

        self.assertEqual(a, b)

    def test_add(self):
        pairs = ((self.first, 1), (self.second, -1))

        source = Multiset(pairs)
        added = source.add(self.first)

        self.assertEqual({self.first: 2, self.second: -1}, added.store)

    def test_add_zero(self):
        pairs = ((self.first, 1), (self.second, -1))

        source = Multiset(pairs)
        added = source.add(self.second)

        self.assertEqual({self.first: 1}, added.store)

    def test_add_compound(self):
        a = Multiset(((self.first, 1), (self.second, -1)))
        b = Multiset(((self.first, -1), (self.second, -1)))

        added = a.add(b)

        self.assertEqual({self.second: -2}, added.store)

    def test_remove(self):
        pairs = ((self.first, 1), (self.second, -1))

        source = Multiset(pairs)
        subtracted = source.remove(self.second)

        self.assertEqual({self.first: 1, self.second: -2}, subtracted.store)

    def test_remove_zero(self):
        pairs = ((self.first, 1), (self.second, -1))

        source = Multiset(pairs)
        subtracted = source.remove(self.first)

        self.assertEqual({self.second: -1}, subtracted.store)

    def test_remove_compound(self):
        a = Multiset(((self.first, 1), (self.second, -1)))
        b = Multiset(((self.first, -1), (self.second, -1)))

        subtracted = a.remove(b)

        self.assertEqual({self.first: 2}, subtracted.store)
