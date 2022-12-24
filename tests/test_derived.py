from pyunitx.derived import parsecs, lightyears


def test_long_distances():
    p = parsecs(1)
    ly = lightyears("3.26156")

    assert p.equivalent_to(ly, 5)
