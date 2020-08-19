import typing
from decimal import Decimal
from numbers import Number

from exceptions import OperationError, ImplicitConversionError


def make_dimension(name: str) -> typing.Type:
    """Create a dimension, a class representing a quantity about the world.
    """

    def new(cls, value):
        if value not in cls.instances:
            cls.instances[value] = super(type, cls).__new__(cls)
        return cls.instances[value]

    def init(self, value):
        if not isinstance(value, Number):
            raise TypeError("A dimension has a scalar value")
        self.value = Decimal(value)

    def add(self, other):
        if not isinstance(other, type(self)):
            raise OperationError("add", type(self), type(other))
        return type(self)(self.value + other.value)

    def subtract(self, other):
        if not isinstance(other, type(self)):
            raise OperationError("subtract", type(self), type(other))
        return type(self)(self.value - other.value)

    def equal(self, other):
        if self is other:
            return True
        if not isinstance(other, self.DIMENSION):
            raise ImplicitConversionError(type(other), type(self))
        return self.value * self.scale == other.value * other.scale

    dimension = type(name, (object,), {
        "__new__": new,
        "__init__": init,
        "__add__": add,
        "__radd__": add,
        "__sub__": subtract,
        "__eq__": equal,
    })

    # can only be defined after the initial class definition
    dimension.DIMENSION = dimension
    return dimension


def make_unit(name: str, dimension: type, scale: typing.Union[Decimal, int]) -> type:
    unit = type(name.title(), (dimension,), {
        "scale": scale,
        "instances": {},
    })

    def converter(self):
        return unit(self.value * self.scale / unit.scale)

    setattr(dimension, "to_" + name, converter)
    return unit
