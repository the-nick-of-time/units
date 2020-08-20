import typing

from exceptions import ImplicitConversionError

Pairs = typing.Tuple[typing.Tuple[type, int], ...]


class Multiset:
    # just different enough from collections.Counter to be worth writing
    def __init__(self, pairs: typing.Union[Pairs, 'Multiset']):
        self.store = pairs.store if isinstance(pairs, Multiset) else dict(pairs)

    def __hash__(self):
        return hash(tuple(self.store.items()))

    def __iter__(self):
        return self.store.keys()

    def __eq__(self, other):
        if isinstance(other, Multiset):
            return self.store == other.store
        return False

    def __contains__(self, item):
        return item in self.store

    def add(self, elem: type):
        if elem in self.store:
            self.store[elem] += 1
        else:
            self.store[elem] = 1

    def remove(self, elem: type):
        if elem in self.store:
            self.store[elem] -= 1
            if self.store[elem] == 0:
                del self.store[elem]
        else:
            self.store[elem] = -1


class CompoundUnit:
    def __init__(self, units: typing.Union[Pairs, Multiset]):
        self.units = Multiset(units)

    def __hash__(self):
        return hash(self.units)

    def __eq__(self, other):
        try:
            return self.units == other.units
        except AttributeError:
            return False

    def __mul__(self, other: type):
        self.__verify_no_dimension_mismatch(other)
        self.units.add(other)

    def __truediv__(self, other: type):
        self.__verify_no_dimension_mismatch(other)
        self.units.remove(other)

    def __verify_no_dimension_mismatch(self, typ: type):
        for unit in self.units:
            if typ is unit:
                break
            elif typ.DIMENSION == unit.DIMENSION:
                # the dimension is already represented in the current unit, but it isn't the
                # same unit
                raise ImplicitConversionError(typ, unit)
