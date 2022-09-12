import typing
from decimal import Decimal
from numbers import Number

from units.exceptions import OperationError, ImplicitConversionError
from units.extras import CompoundUnit, Pairs

ScaleType = typing.Union[Decimal, int]


def make_dimension(name: str) -> typing.Type:
    """Create a dimension, a class representing a quantity about the world.
    """
    dimension = make_compound_dimension(name, ())
    return dimension


def make_unit(name: str, dimension: type, scale: ScaleType) -> type:
    unit = type(name, (dimension,), {
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
        if not other.instance_of(self.DIMENSION):
            raise ImplicitConversionError(type(other), type(self))
        return self.value * self.scale == other.value * other.scale

    def multiply(self, other):
        if isinstance(other, Number):
            return type(self)(self.value * other)
        result_dim = make_compound_dimension(_exponent_name(self, 1) + _exponent_name(other, 1),
                                             (self.UNITS * other.UNITS).units.to_pairs())
        result_unit = make_compound_unit(result_dim, self.scale * other.scale)
        return result_unit(self.value * other.value / (self.scale * other.scale))

    def divide(self, other):
        if isinstance(other, Number):
            return type(self)(self.value / other)
        result_units = (self.UNITS / other.UNITS).units.to_pairs()
        result_value = (self.value / self.scale) / (other.value / other.scale)
        if len(result_units) == 0:
            return result_value
        result_dim = make_compound_dimension(
            _exponent_name(self, 1) + _exponent_name(other, -1),
            result_units)
        result_unit = make_compound_unit(result_dim, self.scale * other.scale)
        return result_unit(result_value)

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
        "__name__": name,
        "instance_of": instance_of,
    })

    # can only be defined after the initial class definition
    dimension.DIMENSION = dimension
    dimension.UNITS = CompoundUnit(exponents if exponents else ((dimension, 1),))

    return dimension


def make_compound_unit(dimension: type, scale: ScaleType):
    name = ""
    for unit in dimension.UNITS:
        name += _exponent_name(unit, dimension.UNITS[unit])

    return make_unit(name, dimension, scale)


def _exponent_name(unit: type, exponent: int) -> str:
    value_names = {
        1: "",
        2: "Squared",
        3: "Cubed",
        4: "ToTheFourth",
        5: "ToTheFifth",
        # that's the highest I've ever seen
    }
    prefix = 'Per' if exponent < 0 else ''
    body = unit.__name__.rstrip("s") if exponent < 0 else unit.__name__
    return f"{prefix}{body}{value_names[abs(exponent)]}"
