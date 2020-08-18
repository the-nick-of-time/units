import typing
from decimal import Decimal
from numbers import Number

from exceptions import OperationError, ImplicitConversionError


def make_dimension(name: str) -> typing.Type:
    """Create a dimension, a class representing a quantity about the world.

    After creating the type and a unit using it, you must set the BASE_UNIT
    class variable on it.
    """

    def new(cls, value):
        if value not in cls.instances:
            cls.instances[value] = super().__new__(cls)
        return cls.instances[value]

    def init(self, value):
        if not isinstance(value, Number):
            raise TypeError("A dimension has a scalar value")
        self.value = value

    def add(self, other):
        if not isinstance(other, type(self)):
            raise OperationError("add", type(self), type(other))
        return type(self)(self.value + other.value)

    def subtract(self, other):
        if not isinstance(other, type(self)):
            raise OperationError("subtract", type(self), type(other))
        return type(self)(self.value - other.value)

    def equal(self, other):
        if not isinstance(other, self.get_dimension()):
            raise ImplicitConversionError(type(other), type(self))
        return self.to_base_unit().value == other.to_base_unit().value

    def to_base_unit(self):
        return self.BASE_UNIT(self.value * self.scale)

    dimension = type(name, (object,), {
        "__new__": new,
        "__init__": init,
        "__add__": add,
        "__radd__": add,
        "__sub__": subtract,
        "__eq__": equal,
        "to_base_unit": to_base_unit,
    })

    # can only be defined after the initial class definition
    def get_dimension(self):
        return dimension

    dimension.get_dimension = get_dimension
    return dimension


def make_unit(name: str, dimension: typing.Type, scale: Decimal) -> typing.Type:
    ...
