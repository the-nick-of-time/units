import typing
from decimal import Decimal
from numbers import Number

from exceptions import OperationError, ImplicitConversionError
from extras import CompoundUnit, Pairs

ScaleType = typing.Union[Decimal, int]


def make_dimension(name: str) -> typing.Type:
    """Create a dimension, a class representing a quantity about the world.
    """
    dimension = make_compound_dimension(name, ())
    return dimension


def make_unit(name: str, dimension: type, scale: ScaleType) -> type:
    unit = type(name.title(), (dimension,), {
        "scale": scale,
        "instances": {},
    })

    def converter(self):
        return unit(self.value * self.scale / unit.scale)

    setattr(dimension, "to_" + name, converter)
    return unit


def make_compound_dimension(name: str, exponents: Pairs) -> type:
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

    def multiply(self, other):
        if isinstance(other, Number):
            return type(self)(self.value * other)
        raise NotImplementedError()

    def divide(self, other):
        if isinstance(other, Number):
            return type(self)(self.value / other)
        raise NotImplementedError()

    def instance_of(self, dim):
        try:
            return dim.DIMENSION.UNITS == self.DIMENSION.UNITS
        except AttributeError:
            return False

    dimension = type(name, (object,), {
        "__new__": new,
        "__init__": init,
        "__add__": add,
        "__radd__": add,
        "__sub__": subtract,
        "__eq__": equal,
        "__mul__": multiply,
        "__truediv__": divide,
        "instance_of": instance_of
    })

    # can only be defined after the initial class definition
    dimension.DIMENSION = dimension
    dimension.UNITS = CompoundUnit(exponents if exponents else ((dimension, 1),))

    return dimension
