import sys

import pytest

from pyunitx.resistor import main


@pytest.mark.parametrize(
    "args,expected",
    [
        [["rgol"], "28.000 kΩ"],
        [["ook"], "33 Ω"],
        [["-t", "ook"], "33 Ω ± 6.6 Ω"],
        [["-s", "rgokvv"], "283 Ω + 0.001415 Ω/K ± 283 mΩ"],
    ]
)
def test_main(monkeypatch, capsys, args, expected):
    with monkeypatch.context() as patch:
        patch.setattr(sys, 'argv', [""] + args)
        main()
        assert capsys.readouterr().out.strip() == expected
