from decimal import Decimal

import pytest

from pyunitx._api import make_unit, make_dimension, make_compound_unit


@pytest.fixture
def BaseDim1():
    return make_dimension("BaseDim1")


@pytest.fixture
def BaseDim2():
    return make_dimension("BaseDim2")


@pytest.fixture
def base_unit_1(BaseDim1):
    return make_unit(name="base_unit_1", dimension=BaseDim1, scale=1, abbrev="b")


@pytest.fixture
def base_unit_2(BaseDim2):
    return make_unit(name="base_unit_2", dimension=BaseDim2, scale=1, abbrev="B")


def test_equivalent_scale(base_unit_1, base_unit_2):
    unit_dec = make_compound_unit(
        name="test_dec",
        scale=Decimal("1.23"),
        abbrev="T",
        exponents={base_unit_1: 1, base_unit_2: 1}
    )
    unit_str = make_compound_unit(
        name="test_str",
        scale="1.23",
        abbrev="t",
        exponents={base_unit_1: 1, base_unit_2: 1}
    )

    assert unit_dec is unit_str
