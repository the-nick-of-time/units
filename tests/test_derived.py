from pyunitx.derived import parsecs, lightyears


def test_long_distances():
    p = parsecs(1)
    l = lightyears("3.26156")

    assert p.equivalent_to(l, 5)
