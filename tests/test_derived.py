from units.derived import parsec, lightyear


def test_long_distances():
    p = parsec(1)
    l = lightyear("3.26156")

    assert p.equivalent_to(l, 1e11)
