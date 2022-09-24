from decimal import Decimal
from numbers import Number
from typing import Type, Dict, Iterator, Sequence, Union, Tuple

from units.exceptions import OperationError, ImplicitConversionError

__all__ = [
    "make_dimension", "make_compound_dimension",
    "make_unit", "make_compound_unit",
]
UnitOperand = Union['UnitInterface', Number]
Scale = Union[Decimal, float, str, Tuple[int, Sequence[int], int]]
Unitlike = Union[Type['UnitInterface'], 'DimensionBase']
Pairs = Tuple[Tuple[Unitlike, int], ...]
Exponents = Union[Pairs, Dict[Unitlike, int]]


def make_dimension(name: str) -> 'DimensionBase':
    """Dimensions are the basic measurable quantities about the world, like length and time.

    For complex dimensions, see make_compound_dimension.

    :param name: The name of this dimension.
    :return: An object that captures information about the dimension and the
        units that implement it.
    """
    dimension = make_compound_dimension((), name)
    return dimension


def make_unit(name: str, dimension: 'DimensionBase', scale: Scale) -> Type['UnitInterface']:
    """A unit is a particular convention for measuring a dimension.

    :param name: The name of the new unit, like "meters". Should be in its
        plural form.
    :param dimension: The dimension this unit measures.
    :param scale: How many of the base unit it would take to get one of the
        current unit. For instance, one kilometer has a scale of 1000 when the
        base unit is meters.
    :return: A class representing the unit. Instances of this class are
        measurements using the unit.
    """

    def new(cls, value: Scale):
        """Create a new measurement using this unit."""
        if value not in cls.instances:
            cls.instances[value] = super(type, cls).__new__(cls)
        instance = cls.instances[value]
        instance.value = Decimal(value)
        return instance

    def add(self, other: UnitInterface) -> UnitInterface:
        """Add two measurements of the same unit together."""
        if type(other).composition != type(self).composition:
            raise OperationError("add", type(self), type(other))
        return type(self)(self.value + other.value * other.scale / self.scale)

    def subtract(self, other: UnitInterface) -> UnitInterface:
        """Subtract a measurement of the same unit from this."""
        if type(other).composition != type(self).composition:
            raise OperationError("subtract", type(self), type(other))
        return type(self)(self.value - other.value * other.scale / self.scale)

    def equal(self, other: UnitInterface) -> bool:
        """Check if this measurement is the same value and unit of another."""
        if self is other:
            return True
        if type(other).composition != type(self).composition:
            return False
        return self.value * self.scale == other.value * other.scale

    def equivalent(self, other: UnitInterface, within=0) -> bool:
        """Check if this measurement is the same dimension as another and that
            its value is equivalent, within a certain precision.

        :param other: The other measurement.
        :param within: An absolute tolerance on the approximation, expressed in
            the base unit.
        :return: Boolean
        """
        if not other.is_dimension(self.dimension):
            raise ImplicitConversionError(type(other), type(self))
        return abs(self.value * self.scale - other.value * other.scale) <= within

    def multiply(self, other: UnitInterface) -> UnitInterface:
        """Multiply two measurements. Produces a new compound unit for the result."""
        if isinstance(other, Number):
            return type(self)(self.value * other)
        dim_composition = self.dimension.composition * other.dimension.composition
        result_dim = make_compound_dimension(dim_composition.to_pairs())
        unit_composition = (self.composition * other.composition).units
        result_unit = make_compound_unit(result_dim, self.scale * other.scale, unit_composition)
        return result_unit(self.value * other.value)

    def divide(self, other: UnitInterface) -> UnitInterface:
        """Multiply two measurements. Produces a new compound unit for the result."""
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

    def is_dimension(self, dim: DimensionBase):
        """Check if this unit is of the given dimension."""
        try:
            return dim.composition == self.dimension.composition
        except AttributeError:
            return False

    def getattribute(self, key: str):
        """Forward conversion requests to the dimension."""
        if key.startswith("to_"):
            return lambda: getattr(self.dimension, key)(self)
        raise AttributeError()

    def tostring(self):
        return f"{self.value * self.scale} {self.__name__}"

    # noinspection PyTypeChecker
    unit: Type[UnitInterface] = type(name, (object,), {
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
        f"""Convert the current unit to {name}"""
        return unit(self.value * self.scale / unit.scale)

    setattr(dimension, "to_" + name.replace(" ", "_"), converter)
    return unit


def make_compound_dimension(exponents: Exponents, name: str = None) -> 'DimensionBase':
    """Create a dimension that's composed of basic dimensions.

    :param exponents: A sequence of tuples or dict that pair existing
        dimensions with the exponent they should be raised to.
    :param name: A name to give this dimension, like velocity for length/time.
        If there isn't a physically useful name for it, leave it unfilled and
        a name will automatically be created by using the names of its
        constituents.
    :return: An object that captures information about the dimension and the
        units that implement it.
    """
    if isinstance(exponents, dict):
        exponents = tuple(exponents.items())
    if name is None:
        name = str(Multiset(exponents))
    dimension = DimensionBase(name, exponents)

    return dimension


def make_compound_unit(dimension: 'DimensionBase', scale: Scale, exponents: Exponents,
                       name: str = None):
    """A unit composed of other units.

    :param dimension: The dimension this unit is measuring.
    :param scale: How many of the base unit one of this unit is equivalent to.
        Note that the scale factors of the constituent units are not taken into
        account. For instance, even though the conversion factor from meters per
        second to miles per hour could be determined strictly from the scale
        factors already defined for miles -> meters and hours -> seconds, doing
        that calculation is up to the constructor of the unit. I think this
        obeys the principle of least surprise, but I might be wrong.
    :param exponents: A sequence of tuples or dict that pair existing units
        with the exponent they should be raised to.
    :param name: A name to give this unit, like joules. If no particular
        physical name exists, leave it unfilled and a name will be automatically
        constructed using the names of its component units and their exponents.
    :return: A class representing this unit. Instances of the class are
        measurements with a magnitude.
    """
    if isinstance(exponents, dict):
        exponents = tuple(exponents.items())
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
    def __init__(self, pairs: Union[Pairs, 'Multiset', dict]):
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

    def __iter__(self) -> Iterator[Unitlike]:
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

    def add(self, elem: Union[type, 'Multiset']):
        if isinstance(elem, type):
            elem = Multiset({elem: 1})
        return self.__merge(elem)

    def remove(self, elem: Union[type, 'Multiset']):
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
    def __init__(self, units: Union[Pairs, Multiset]):
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

    def __mul__(self, other: Union[type, Multiset, 'Compound']) -> 'Compound':
        if isinstance(other, type):
            other = Multiset({other: 1})
        elif isinstance(other, Compound):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return Compound(self.units.add(other))

    def __truediv__(self, other: Union[type, Multiset, 'Compound']) -> 'Compound':
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


class UnitInterface:
    """A dummy class for type checking purposes, defining the interface of a unit class."""
    composition: 'Compound'
    scale: 'Decimal'

    def __init__(self, value: Scale):
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
