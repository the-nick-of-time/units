from units.pressure import psi, bars


def test_conversion():
    imperial = psi(43)
    equivalent = bars(3)
    assert imperial.to_bars().sig_figs(2) == equivalent
