import re
import textwrap
from decimal import Decimal
from numbers import Number
from typing import Union, Tuple, Sequence, Type, Dict, Iterator

import sigfig

from pyunitx._exceptions import OperationError, ImplicitConversionError

__all__ = [
    "make_dimension",
    "make_unit",
    "make_compound_dimension",
    "make_compound_unit",
    "SIUNITX_NEW",
    "SIUNITX_OLD",
]
UnitOperand = Union['UnitInterface', Number]
Scale = Union[Decimal, float, str, Tuple[int, Sequence[int], int]]
Unitlike = Union[Type['UnitInterface'], 'DimensionBase']
Pair = Tuple[Unitlike, int]
Pairs = Tuple[Pair, ...]
Exponents = Union[Pairs, Dict[Unitlike, int]]

SIUNITX_NEW = 3
SIUNITX_OLD = 2


def make_dimension(name: str) -> 'DimensionBase':
    """Dimensions are the basic measurable quantities about the world, like length and time.

    For complex dimensions, see make_compound_dimension.

    :param name: The name of this dimension.
    :return: An object that captures information about the dimension and the
        units that implement it.
    """
    dimension = make_compound_dimension((), name)
    return dimension


def make_unit(*, name: str, dimension: 'DimensionBase', scale: Scale, abbrev, doc="") -> Type[
    'UnitInterface']:
    """A unit is a particular convention for measuring a dimension.

    The resulting class represents the abstract concept of the unit, say meters.
    Instances of the class associate that unit with a number, defining in this
    example a particular length like 8 meters. Instances of a unit class are
    called "measurements" within this documentation.

    :param name: The name of the new unit, like "meters". Should be in its
        plural form.
    :param dimension: The dimension this unit measures.
    :param scale: How many of the base unit it would take to get one of the
        current unit. For instance, one kilometer has a scale of 1000 when the
        base unit is meters.
    :param abbrev: The canonical abbreviation for this unit, like "lb" for
        pounds or "g" for grams. Used for output.
    :param doc: Documentation for this unit, optional.
    :return: A class representing the unit. Instances of this class are
        measurements using the unit.
    """

    def new(cls, value: Scale):
        """Create a new measurement using this unit.

        Instances are flyweights; two invocations of meters(1) will return the
        same object.
        """
        if value not in cls.instances:
            cls.instances[value] = super(type, cls).__new__(cls)
        instance = cls.instances[value]
        instance.value = Decimal(value)
        return instance

    def add(self, other: UnitInterface) -> UnitInterface:
        """Add two measurements of the same unit together.

        Checks compatibility rather than type for determining "same unit". For
        example, a calculation that outputs the dynamically created unit
        kg*m*s^-2 is equivalent to a defined expression using newtons.

        :param other: Another measurement, with the same units
        """
        if type(other).composition != type(self).composition:
            raise OperationError("add", type(self), type(other))
        return type(self)(self.value + other.value * other.scale / self.scale)

    def subtract(self, other: UnitInterface) -> UnitInterface:
        """Subtract a measurement of the same unit from this.

        Checks compatibility rather than type for determining "same unit". For
        example, a calculation that outputs the dynamically created unit
        kg*m*s^-2 is equivalent to a defined expression using newtons.

        :param other: Another measurement, with the same units
        """
        if type(other).composition != type(self).composition:
            raise OperationError("subtract", type(self), type(other))
        return type(self)(self.value - other.value * other.scale / self.scale)

    def equal(self, other: UnitInterface) -> bool:
        """Check if this measurement is the same value and unit of another.

        Checks compatibility rather than type for determining "same unit". For
        example, a calculation that outputs the dynamically created unit
        kg*m*s^-2 is equivalent to a defined expression using newtons.
        """
        if self is other:
            return True
        if type(other).composition != type(self).composition:
            return False
        return self.value * self.scale == other.value * other.scale

    def equivalent(self, other: UnitInterface, within=0) -> bool:
        """Check if this measurement represents the same quantity as another,
        within a certain precision.

        You can think of it as converting both measurements to their shared base
        unit, then checking whether they are within the specified difference of
        each other.

        :param other: The other measurement.
        :param within: An absolute tolerance on the approximation, expressed in
            the base unit.
        :return: Whether the two measurements are approximately equal.
        """
        if not other.is_dimension(self.dimension):
            raise ImplicitConversionError(type(other), type(self))
        return abs(self.value * self.scale - other.value * other.scale) <= within

    def multiply(self, other: Union[UnitInterface, int, float, Decimal]) -> UnitInterface:
        """Multiply two measurements. Produces a new compound unit for the result.

        If the two quantities completely cancel (like a frequency times a
        duration), the result will be returned as a plain number.

        :param other: Another measurement, with any units.
        :return: The result of the calculation, with the compound units.
        """
        if isinstance(other, (int, float, Decimal)):
            return type(self)(self.value * Decimal(other))
        result_value = self.value * other.value
        unit_composition = (self.composition * other.composition).units
        if len(unit_composition) == 0:
            return result_value
        result_unit = make_compound_unit(
            scale=self.scale * other.scale,
            exponents=unit_composition
        )
        return result_unit(result_value)

    def divide(self, other: Union[UnitInterface, int, float, Decimal]) -> UnitInterface:
        """Multiply two measurements. Produces a new compound unit for the result.

        :param other: Another measurement, with any units.
        """
        if isinstance(other, (int, float, Decimal)):
            return type(self)(self.value / Decimal(other))
        result_units = self.composition / other.composition
        result_value = self.value / other.value
        if len(result_units) == 0:
            return result_value
        result_unit = make_compound_unit(
            scale=self.scale / other.scale,
            exponents=result_units.to_pairs()
        )
        return result_unit(result_value)

    def exponent(self, other: Scale) -> UnitInterface:
        """Raise this measurement to a power such that the result has no
        non-integer exponents.

        For instance, ``meters(4) ** 2 == meters_squared(16)``. You can also
        compute the magnitude of a vector with
        ``vec = [meters(4), meters(3)]; mag = (vec[0] ** 2 + vec[1] ** 2) ** (1/2)``.

        If the resulting calculation has any units with non-integer powers,
        ``ValueError`` is raised.

        :param other: Any integer, the power to raise this measurement to.
        :raises ValueError: If the resulting unit has fractional exponents.
        :return: A measurement with the value and units raised to the power.
        """
        result_composition = self.composition ** other
        result_value = self.value ** Decimal(other)
        result_unit = make_compound_unit(
            scale=self.scale ** Decimal(other),
            exponents=result_composition.to_pairs()
        )
        return result_unit(result_value)

    def is_dimension(self, dim: DimensionBase):
        """Check if this unit is of the given dimension.

        Most useful for checking whether two measurements can be reasonably
        compared with ``.equivalent_to`` or converted into the other.

        :param dim: The dimension to
        :return: Whether this unit is of the given dimension.
        """
        try:
            return dim.composition == self.dimension.composition
        except AttributeError:
            return False

    def getattribute(self, key: str):
        """Forward conversion requests to the dimension.

        The dimension, being the one thing all compatible units have in common,
        is the logical place to store all conversion functions between different
        units.

        Any ``x.to_*`` method calls are therefore passed to the dimension.

        :param key: The method name.
        :return: A pseudo-bound method of the conversion function.
        :raise AttributeError: If the requested method doesn't look like a
            conversion function, or if there isn't a conversion function by that
            name.
        """
        if key.startswith("to_"):
            return lambda: getattr(self.dimension, key)(self)
        raise AttributeError()

    def tostring(self):
        return f"{self.value} {self.abbreviation}"

    def sig_figs(self, figs=3) -> UnitInterface:
        """Produce a version of this measurement rounded to significant figures.

        :param figs: How many significant figures to round to.
        :return: A new measurement with a rounded value.
        """
        rounded = sigfig.round(self.value, sigfigs=figs)
        return type(self)(rounded)

    def to_latex(self, siunitx_major_version=SIUNITX_NEW):
        r"""Output this unit value as it would be used in LaTeX with siunitx.

        Maybe script your calculations, then write the output to a .tex file
        and include it in your main document.

        :param siunitx_major_version: siunitx changed the name of its macro
            that outputs a number with a unit in version 3.0. Prior, it was
            ``\SI{number}{units}``, and after it was ``\qty{number}{units}``.
            Defaults to the most recent version. If you're using an older one,
            for instance if your TeXLive distribution is a few years old, pass
            in :data:`pyunitx.SIUNITX_OLD`, an alias for 2. I doubt anyone is
            using version 1.
        :return: A string formatted for direct inclusion in LaTeX.
        """
        if siunitx_major_version >= 3:
            fmt = r"\qty{{{value}}}{{{unit}}}"
        else:
            fmt = r"\SI{{{value}}}{{{unit}}}"
        if re.match(r"^\w+$", self.abbreviation):
            # This unit has an elementary name, like J for joules
            return fmt.format(value=self.value, unit=self.abbreviation)
        units = []
        for u, e in self.composition.to_pairs():
            if e == 1:
                units.append(u.abbreviation)
            else:
                units.append(f"{u.abbreviation}^{{{e}}}")
        return fmt.format(value=self.value, unit=".".join(units))

    # @formatter:off
    # noinspection PyTypeChecker
    unit: Type[UnitInterface] = type(name, (object,), {
        "__new__": new,
        "__add__": add,
        "__radd__": add,
        "__sub__": subtract,
        "__eq__": equal,
        "__mul__": multiply,
        "__rmul__": multiply,
        "__truediv__": divide,
        "__rtruediv__": divide,
        "__getattr__": getattribute,
        "__str__": tostring,
        "__repr__": tostring,
        "__pow__": exponent,
        "__name__": name,
        "__doc__": textwrap.dedent(doc),
        "is_dimension": is_dimension,
        "scale": Decimal(scale),
        "instances": {},
        "dimension": dimension,
        "equivalent_to": equivalent,
        "sig_figs": sig_figs,
        "abbreviation": abbrev,
        "to_latex": to_latex,
    })
    # @formatter:on
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


def make_compound_unit(*, scale: Scale, exponents: Exponents, name: str = None, abbrev=None,
                       doc=""):
    """A unit composed of other units.

    :param abbrev:
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
    :param doc: Documentation for this unit, to show in tools like Sphinx.
    :return: A class representing this unit. Instances of the class are
        measurements with a magnitude.
    """
    if isinstance(exponents, dict):
        exponents = tuple(exponents.items())
    if name is None:
        name = str(Multiset(exponents))
    composition = Compound(exponents)
    dims_extracted = tuple((unit.dimension, exp) for unit, exp in composition.to_pairs())
    dims = _sort(_dedupe(dims_extracted))
    dimension = make_compound_dimension(dims)
    unit = make_unit(
        name=name,
        dimension=dimension,
        scale=scale,
        abbrev=abbrev if abbrev is not None else composition.make_abbreviation(),
        doc=doc
    )
    unit.composition = composition
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
    return _sort(accumulator)


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


def _dedupe(pairs: Iterator[Pair]) -> Dict[Unitlike, int]:
    accumulator = {}
    for unitish, num in pairs:
        if unitish in accumulator:
            accumulator[unitish] += num
        else:
            accumulator[unitish] = num
    return accumulator


def _sort(d: Union[Exponents, Iterator[Pair]]) -> Pairs:
    if isinstance(d, dict):
        pairs = tuple(d.items())
    else:
        pairs = d
    return tuple(sorted(pairs, key=lambda p: (-p[1], p[0].__name__)))


class DimensionBase:
    __INSTANCES = {}

    def __new__(cls, name: str, exponents: Pairs):
        exponents = tuple((k, v) for k, v in exponents if v != 0)
        if len(exponents) == 0:
            # Base dimensions are identified by name
            key = name
        elif len(exponents) == 1 and exponents[0][1] == 1:
            # If you end up with a base unit after a calculation
            decomposed = _decompose_all(exponents)
            if len(decomposed) == 1 and decomposed[0][1] == 1:
                key = name
            else:
                key = decomposed
        else:
            # Compound dimensions with the same base dimensions must refer to the same thing
            key = _decompose_all(exponents)
        if key not in cls.__INSTANCES:
            cls.__INSTANCES[key] = super(DimensionBase, cls).__new__(cls)
        this = cls.__INSTANCES[key]
        this.__name__ = name
        this.composition = Compound(exponents or ((this, 1),))
        return this

    def __hash__(self):
        return hash(self.__name__)

    def __repr__(self):
        return self.__name__


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
            self.store = _dedupe(pairs)
        self.store = {k: v for k, v in self.store.items() if v != 0}

    def __iter__(self) -> Iterator[Unitlike]:
        return iter(self.store.keys())

    def __getitem__(self, item):
        return self.store[item]

    def __eq__(self, other):
        if isinstance(other, Multiset):
            return self.store == other.store
        return False

    def __len__(self):
        return len(self.store)

    def __str__(self):
        names = [_exponent_name(k, v) for k, v in _sort(self.store)]
        return "_".join(names)

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
        return _sort((key, self[key]) for key in self)

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


class Compound:
    def __init__(self, units: Union[Pairs, Multiset]):
        if isinstance(units, Multiset):
            self.units = Multiset(units)
        else:
            decomposed = _decompose_all(units)
            self.units = Multiset(decomposed)

    def __eq__(self, other):
        try:
            return self.units == other.units
        except AttributeError:
            return False

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
            other = Multiset({other: 1})
        elif isinstance(other, Compound):
            other = other.units
        self.__verify_no_dimension_mismatch(other)
        return Compound(self.units.remove(other))

    def __pow__(self, power: Union[int, float, Decimal]):
        pairs = []
        for t, e in self.to_pairs():
            new_exponent = e * power
            if int(new_exponent) != new_exponent:
                raise ValueError(
                    f"The exponentiation has caused a non-integer exponent on {t}, "
                    f"which is not allowed."
                )
            pairs.append((t, new_exponent))
        return Compound(tuple(pairs))

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

    def make_abbreviation(self) -> str:
        ordered = _sort(self.to_pairs())
        chunks = []
        for unit, exponent in ordered:
            if exponent == 1:
                chunks.append(unit.abbreviation)
            else:
                chunks.append(f"{unit.abbreviation}^{exponent}")
        return " ".join(chunks)


class UnitInterface:
    """A dummy class for type checking purposes, defining the interface of a unit class."""
    composition: 'Compound'
    scale: 'Decimal'
    abbreviation: str
    __slots__ = ["value"]

    def __init__(self, value: Scale):
        ...

    def __add__(self, other: UnitOperand) -> 'UnitInterface':
        ...

    def __sub__(self, other: UnitOperand) -> 'UnitInterface':
        ...

    def __mul__(self, other: UnitOperand) -> 'UnitInterface':
        ...

    def __truediv__(self, other: UnitOperand) -> 'UnitInterface':
        ...

    def is_dimension(self, dim: DimensionBase) -> bool:
        ...

    def equivalent_to(self, quantity: 'UnitInterface', within=0) -> bool:
        ...

    def sig_figs(self, figures=3):
        ...
