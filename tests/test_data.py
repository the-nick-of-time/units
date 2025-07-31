from pyunitx.data import megabytes, bits

def test_si():
    assert bits(8_000_000).to_megabytes() == megabytes(1)
