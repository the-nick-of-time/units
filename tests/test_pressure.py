from pyunitx.pressure import psi, bars, Pressure


def test_conversion():
    imperial = psi(43)
    equivalent = bars(3)
    assert imperial.to_bars().sig_figs(2) == equivalent


def test_dimension():
    assert bars(1).is_dimension(Pressure)
