from project.context_free.cfg import *
from project.context_free.ecfg import *
from project.regular.graph_utils import create_dfa_by_regex


def test_ecfg_from_cfg():
    try:
        cfg = read_cfg_from_file("tests/test_files/cfg_1.txt")
    except OSError:
        cfg = read_cfg_from_file("test_files/cfg_1.txt")
    ecfg = ECFG.ecfg_from_cfg(cfg)

    expected_ecfg = ECFG(
        variables={Variable("S"), Variable("A")},
        start_symbol=Variable("S"),
        productions={
            Variable("S"): Regex("A"),
            Variable("A"): Regex("(($|b?)|(S.S))"),
        },
    )

    assert ecfg.variables == expected_ecfg.variables
    assert ecfg.start_symbol == expected_ecfg.start_symbol
    assert all(
        create_dfa_by_regex(ecfg.productions[var]).is_equivalent_to(
            create_dfa_by_regex(expected_ecfg.productions[var])
        )
        for var in expected_ecfg.productions.keys()
    )


def test_ecfg_from_text_empty():
    ecfg = ECFG.ecfg_from_text("")

    assert ecfg.productions == {}


def test_ecfg_from_text_nonempty():
    ecfg = ECFG.ecfg_from_text(
        """
        S -> A B C* | a b
        A -> a*
        B -> b
        C -> c | b
        """
    )

    expected_ecfg = ECFG(
        variables={Variable("S"), Variable("A"), Variable("B"), Variable("C")},
        start_symbol=Variable("S"),
        productions={
            Variable("S"): Regex("((A.(B.(C)*))|(a.b))"),
            Variable("A"): Regex("(a)*"),
            Variable("B"): Regex("b"),
            Variable("C"): Regex("(c|b)"),
        },
    )

    assert ecfg.variables == expected_ecfg.variables
    assert ecfg.start_symbol == expected_ecfg.start_symbol
    assert all(
        create_dfa_by_regex(ecfg.productions[var]).is_equivalent_to(
            create_dfa_by_regex(expected_ecfg.productions[var])
        )
        for var in expected_ecfg.productions.keys()
    )
