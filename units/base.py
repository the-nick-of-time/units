import typing
from decimal import Decimal
from numbers import Number

from units.exceptions import OperationError, ImplicitConversionError


def make_dimension(name: str) -> 'DimensionBase':
    """Create a dimension, a class representing a quantity about the world.
    """
    dimension = make_compound_dimension((), name)
    return dimension


def make_unit(name: str, dimension: 'DimensionBase', scale) -> typing.Type['UnitInterface']:
    def new(cls, value):
        if value not in cls.instances:
            cls.instances[value] = super(type, cls).__new__(cls)
        instance = cls.instances[value]
        instance.value = Decimal(value)
        return instance

    def add(self, other):
        if type(other).composition != type(self).composition:
            raise OperationError("add", type(self), type(other))
        return type(self)(self.value + other.value)

    def subtract(self, other):
        if type(other).composition != type(self).composition:
            raise OperationError("subtract", type(self), type(other))
        return type(self)(self.value - other.value)

    def equal(self, other):
        if self is other:
            return True
        if type(other).composition != type(self).composition:
            return False
        return self.value * self.scale == other.value * other.scale

    def equivalent(self, other, within=0):
        if not other.is_dimension(self.dimension):
            raise ImplicitConversionError(type(other), type(self))
        return abs(self.value * self.scale - other.value * other.scale) <= within

    def multiply(self, other):
        if isinstance(other, Number):
            return type(self)(self.value * other)
        dim_composition = self.dimension.composition * other.dimension.composition
        result_dim = make_compound_dimension(dim_composition.to_pairs())
        unit_composition = (self.composition * other.composition).units
        result_unit = make_compound_unit(result_dim, self.scale * other.scale, unit_composition)
        return result_unit(self.value * other.value)

    def divide(self, other):
        if isinstance(other, Number):
            return type(self)(self.value / other)
        result_units = self.composition / other.composition
        result_value = (self.value / self.scale) / (other.value / other.scale)
        if len(result_units) == 0:
            return result_value
        dim_composition = self.dimension.composition / other.dimension.composition
        result_dim = make_compound_dimension(dim_composition.to_pairs())
        result_unit = make_compound_unit(result_dim, self.scale / other.scale,
                                         result_units.to_pairs())
        return result_unit(result_value)

    def is_dimension(self, dim):
        try:
            return dim.composition == self.dimension.composition
        except AttributeError:
            return False

    def getattribute(self, key: str):
        if key.startswith("to_"):
            return lambda: getattr(self.dimension, key)(self)
        raise AttributeError()

    def tostring(self):
        return f"{self.value} {self.__name__}"

    # noinspection PyTypeChecker
    unit: typing.Type[UnitInterface] = type(name, (object,), {
        "__new__": new,
        "__add__": add,
        "__radd__": add,
        "__sub__": subtract,
        "__eq__": equal,
        "__mul__": multiply,
        "__truediv__": divide,
        "__getattr__": getattribute,
        "__str__": tostring,
        "__repr__": tostring,
        "__name__": name,
        "is_dimension": is_dimension,
        "scale": Decimal(scale),
        "instances": {},
        "dimension": dimension,
        "equivalent_to": equivalent,
    })
    unit.composition = Compound(((unit, 1),))

    def converter(self):
        return unit(self.value * self.scale / unit.scale)

    setattr(dimension, "to_" + name, converter)
    return unit


Unitlike = typing.Union[typing.Type['UnitInterface'], 'DimensionBase']
Pairs = typing.Tuple[typing.Tuple[Unitlike, int], ...]


def make_compound_dimension(exponents: Pairs, name: str = None) -> 'DimensionBase':
    if name is None:
        name = str(Multiset(exponents))
    dimension = DimensionBase(name, exponents)

    return dimension


def make_compound_unit(dimension: 'DimensionBase', scale, exponents: Pairs, name: str = None):
    if name is None:
        name = str(Multiset(exponents))
    unit = make_unit(name, dimension, scale)
    unit.composition = Compound(exponents)
    return unit


def _exponent_name(unit: type, exponent: int) -> str:
    value_names = {
        1: "",
        2: "_squared",
        3: "_cubed",
        4: "_to_the_fourth",
        5: "_to_the_fifth",
        # that's the highest I've ever seen
    }
    prefix = 'per_' if exponent < 0 else ''
    body = unit.__name__.rstrip("s") if exponent < 0 else unit.__name__
    return f"{prefix}{body}{value_names[abs(exponent)]}"


def _decompose_all(exponents: Pairs) -> Pairs:
    accumulator = []
    for unitish, exponent in exponents:
        accumulator.extend(_decompose(unitish, exponent))
    return tuple(sorted(accumulator, key=lambda p: (-p[1], p[0].__name__)))


def _decompose(unit: Unitlike, factor: int) -> Pairs:
    if not hasattr(unit, "composition"):
        # must be a unit currently under construction and doesn't have composition yet
        return (unit, factor),
    if len(unit.composition) == 1:
        return tuple((k, e * factor) for k, e in unit.composition.to_pairs())
    accumulator = []
    for k, e in unit.composition.to_pairs():
        accumulator.extend(_decompose(k, e * factor))
    return tuple(accumulator)


class DimensionBase:
    __INSTANCES = {}

    def __new__(cls, name: str, exponents: Pairs):
        if len(exponents) == 0:
            # Base dimensions are identified by name
            key = name
        else:
            # Compound dimensions with the same base dimensions must refer to the same thing
            key = _decompose_all(exponents)
        if key not in cls.__INSTANCES:
            cls.__INSTANCES[key] = super(DimensionBase, cls).__new__(cls)
        this = cls.__INSTANCES[key]
        this.__name__ = name
        this.composition = Compound(exponents or ((this, 1),))
        this.dimension = this
        return this

    def __hash__(self):
        return hash(self.__name__)


class Multiset:
    # just different enough from collections.Counter to be worth writing
    def __init__(self, pairs: typing.Union[Pairs, 'Multiset', dict]):
        if isinstance(pairs, Multiset):
            self.store = pairs.store.copy()
        # Split these cases from each other just because it makes pycharm's
        # type inference work properly
        elif isinstance(pairs, dict):
            self.store = pairs.copy()
        else:
            self.store = self.__dedupe(pairs)

    def __hash__(self):
        return hash(tuple(self.store.items()))

    def __iter__(self) -> typing.Iterator[Unitlike]:
        return iter(self.store.keys())

    def __getitem__(self, item):
        return self.store[item]

    def __eq__(self, other):
        if isinstance(other, Multiset):
            return self.store == other.store
        return False

    def __contains__(self, item):
        return item in self.store

    def __len__(self):
        return len(self.store)

    def __str__(self):
        positives = [_exponent_name(k, v) for k, v in self.store.items() if v > 0]
        negatives = [_exponent_name(k, v) for k, v in self.store.items() if v < 0]
        return "_".join(positives + negatives)

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

    def to_pairs(self) -> Pairs:
        return tuple((key, self[key]) for key in self)

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

    @staticmethod
    def __dedupe(pairs: Pairs):
        accumulator = {}
        for unitish, num in pairs:
            if unitish in accumulator:
                accumulator[unitish] += num
            else:
                accumulator[unitish] = num
        return accumulator


class Compound:
    def __init__(self, units: typing.Union[Pairs, Multiset]):
        if isinstance(units, Multiset):
            self.units = Multiset(units)
        else:
            decomposed = _decompose_all(units)
            self.units = Multiset(decomposed)

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

    def __len__(self):
        return len(self.units)

    def __mul__(self, other: typing.Union[type, Multiset, 'Compound']) -> 'Compound':
        if isinstance(other, type):
            other = Multiset({other: 1})
        elif isinstance(other, Compound):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return Compound(self.units.add(other))

    def __truediv__(self, other: typing.Union[type, Multiset, 'Compound']) -> 'Compound':
        if isinstance(other, type):
            other = Multiset({other: -1})
        elif isinstance(other, Compound):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return Compound(self.units.remove(other))

    def __verify_no_dimension_mismatch(self, extra: Multiset):
        existing_dimensions = {unit.dimension: unit for unit in self.units}
        for unit in extra:
            if (unit.dimension in existing_dimensions
                    and existing_dimensions[unit.dimension] is not unit):
                # the dimension is already represented in the current unit, but it isn't the
                # same unit
                raise ImplicitConversionError(unit, existing_dimensions[unit.dimension])

    def to_pairs(self):
        return self.units.to_pairs()


UnitOperand = typing.Union['UnitInterface', Number]


class UnitInterface:
    """A dummy class for type checking purposes, defining the interface of a unit class."""
    composition: 'Compound'
    scale: 'Decimal'

    def __init__(self, value):
        pass

    def __add__(self, other: UnitOperand) -> 'UnitInterface':
        pass

    def __sub__(self, other: UnitOperand) -> 'UnitInterface':
        pass

    def __mul__(self, other: UnitOperand) -> 'UnitInterface':
        pass

    def __truediv__(self, other: UnitOperand) -> 'UnitInterface':
        pass

    def is_dimension(self, dim: DimensionBase) -> bool:
        pass

    def equivalent_to(self, quantity: 'UnitInterface') -> bool:
        pass
