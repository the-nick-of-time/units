import sys

import pytest

from pyunitx._api import Compound
from pyunitx.mass import kilograms
from pyunitx.time import seconds
from pyunitx.uconvert import parse_unit, main
from pyunitx.volume import fluid_ounces


@pytest.mark.parametrize(
    "spec,expected", [
        ("kg", ((kilograms, 1),)),
        ("s^-2", ((seconds, -2),)),
        ("fl oz^2", ((fluid_ounces, 2),)),
        ("kg.s^-1", ((kilograms, 1), (seconds, -1))),
    ]
)
def test_parse_unit_success(spec, expected):
    c = parse_unit(spec)

    assert c == Compound(expected)


def test_parse_unit_fail():
    with pytest.raises(KeyError):
        parse_unit("lN")


@pytest.mark.parametrize(
    "args,expected", [
        (["10", "kg", "lbm_A"], "22.0462 lbm_A"),
        (["-f", "3", "10", "kg", "lbm_A"], "22.0 lbm_A"),
        (["10", "m.s^-1", "mi.hr^-1"], "22.3694 mi hr^-1"),
    ]
)
def test_main(monkeypatch, capsys, args, expected):
    with monkeypatch.context() as patch:
        patch.setattr(sys, 'argv', [""] + args)
        main()
        assert capsys.readouterr().out.strip() == expected


@pytest.mark.parametrize(
    "args", [
        ["10", "kg", "mi"],
        ["10", "kg.mol^-1", "mol.kg^-1"],
    ]
)
def test_main_fail(monkeypatch, capsys, args):
    with monkeypatch.context() as patch:
        patch.setattr(sys, 'argv', [""] + args)
        with pytest.raises(TypeError):
            main()
