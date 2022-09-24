from units.energy import joules
from units.force import pounds, kgf, newtons
from units.length import meters
from units.pressure import bars


def test_equivalence():
    assert kgf(1).equivalent_to(pounds(2.2), .05)


def test_complex_addition():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100)

    expected = newtons(1200100)
    assert area * pressure + extra_force == expected


def test_complex_subtraction():
    area = meters(2) * meters(2)
    pressure = bars(3)
    extra_force = newtons(100000)

    expected = newtons(1100000)
    assert area * pressure - extra_force == expected


def test_work():
    displacement = meters(2)
    force = newtons(10)
    expected = joules(20)

    assert displacement * force == expected
