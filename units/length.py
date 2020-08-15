from decimal import Decimal
from numbers import Number

from exceptions import OperationError


class Length:
    __slots__ = 'value', 'scale'

    def __init__(self, value):
        if not isinstance(value, Number):
            raise TypeError("A length is a scalar number")
        self.value = value

    def __add__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self.value + other.value)
        raise OperationError("add", type(self), type(other))

    def __sub__(self, other):
        if isinstance(other, type(self)):
            return type(self)(self.value - other.value)
        raise OperationError("add", type(self), type(other))

    def __eq__(self, other):
        if isinstance(other, Length):
            return self._to_base_unit().value == other._to_base_unit().value

    def _base_unit(self):
        return Meters

    def _to_base_unit(self):
        return self._base_unit()(self.value * self.scale)

    def to_meters(self):
        return self._to_base_unit()

    def to_kilometers(self):
        return Kilometers(self._to_base_unit().value / self.scale)

    def to_feet(self):
        return Feet(self._to_base_unit().value / self.scale)


class Meters(Length):
    scale = Decimal("1")


class Kilometers(Length):
    scale = Decimal("1000")


class Feet(Length):
    scale = Decimal("0.3048")
