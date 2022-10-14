from pyunitx.power import watts, Power, kilowatts, horsepower


def test_dimension():
    assert watts(1).is_dimension(Power)


def test_conversion():
    assert kilowatts(2).to_horsepower().sig_figs(3) == horsepower("2.68")


def test_automatic_converter_ordering():
    core = kilowatts(1)

    v = core.to_feet_pounds_per_second()
    assert v.sig_figs(3) == type(v)("738")
    assert core.to_pounds_feet_per_second().sig_figs() == type(v)("738")
