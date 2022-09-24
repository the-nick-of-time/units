from units.force import pounds, kgf


def test_equivalence():
    assert kgf(1).equivalent_to(pounds(2.2), .05)
