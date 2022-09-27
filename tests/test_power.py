from units.power import watts, Power, kilowatts, horsepower


def test_dimension():
    assert watts(1).is_dimension(Power)


def test_conversion():
    assert kilowatts(2).to_horsepower().sig_figs(3) == horsepower("2.68")
