import typing

from exceptions import ImplicitConversionError

Pairs = typing.Tuple[typing.Tuple[type, int], ...]


class Multiset:
    # just different enough from collections.Counter to be worth writing
    def __init__(self, pairs: typing.Union[Pairs, 'Multiset', dict]):
        self.store = pairs.store.copy() if isinstance(pairs, Multiset) else dict(pairs)

    def __hash__(self):
        return hash(tuple(self.store.items()))

    def __iter__(self):
        return iter(self.store.keys())

    def __getitem__(self, item):
        return self.store[item]

    def __eq__(self, other):
        if isinstance(other, Multiset):
            return self.store == other.store
        return False

    def __contains__(self, item):
        return item in self.store

    def add(self, elem: typing.Union[type, 'Multiset']):
        if isinstance(elem, type):
            elem = Multiset({elem: 1})
        return self.__merge(elem)

    def remove(self, elem: typing.Union[type, 'Multiset']):
        if isinstance(elem, type):
            elem = Multiset({elem: -1})
        else:
            elem = Multiset({key: -value for key, value in elem.store.items()})
        return self.__merge(elem)

    def __merge(self, other: 'Multiset') -> 'Multiset':
        copy = self.store.copy()
        for key in other:
            if key in copy:
                copy[key] += other[key]
            else:
                copy[key] = other[key]
            if copy[key] == 0:
                del copy[key]
        return Multiset(copy)


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

    def __iter__(self):
        return iter(self.units)

    def __getitem__(self, item):
        return self.units[item]

    def __mul__(self, other: typing.Union[type, Multiset, 'CompoundUnit']):
        if isinstance(other, type):
            other = Multiset({other: 1})
        elif isinstance(other, CompoundUnit):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return CompoundUnit(self.units.add(other))

    def __truediv__(self, other: typing.Union[type, Multiset, 'CompoundUnit']):
        if isinstance(other, type):
            other = Multiset({other: -1})
        elif isinstance(other, CompoundUnit):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return CompoundUnit(self.units.remove(other))

    def __verify_no_dimension_mismatch(self, extra: Multiset):
        existing_dimensions = {unit.DIMENSION: unit for unit in self.units}
        for unit in extra:
            if (unit.DIMENSION in existing_dimensions
                    and existing_dimensions[unit.DIMENSION] is not unit):
                # the dimension is already represented in the current unit, but it isn't the
                # same unit
                raise ImplicitConversionError(unit, existing_dimensions[unit.DIMENSION])
