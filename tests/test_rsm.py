from project.regular.graph_utils import create_dfa_by_regex
from project.context_free.ecfg import *
from project.context_free.rsm import *


def test_rsm_from_ecfg_empty():
    ecfg = ECFG.ecfg_from_text("")
    rsm = RSM.rsm_from_ecfg(ecfg)

    expected_productions = {}

    assert all(
        rsm.boxes[var].is_equivalent_to(expected_productions[var].to_epsilon_nfa())
        for var in expected_productions.keys()
    )


def test_rsm_from_ecfg():
    try:
        ecfg = ECFG.ecfg_from_file("tests/test_files/ecfg_1.txt")
    except OSError:
        ecfg = ECFG.ecfg_from_file("test_files/ecfg_1.txt")
    rsm = RSM.rsm_from_ecfg(ecfg)

    expected_productions = {
        Variable("S"): Regex("A B C"),
        Variable("A"): Regex("a"),
        Variable("B"): Regex("b"),
        Variable("C"): Regex("(c | S)"),
    }

    assert rsm.start_symbol == Variable("S")
    assert all(
        rsm.boxes[var].is_equivalent_to(expected_productions[var].to_epsilon_nfa())
        for var in expected_productions.keys()
    )


def test_rsm_from_ecfg_equivalent_languages():
    ecfg = ECFG.ecfg_from_text(
        """
        S -> A B C* | a b
        A -> a*
        B -> b
        C -> c | b
        """
    )

    rsm = RSM.rsm_from_ecfg(ecfg)

    assert len(rsm.boxes) == len(ecfg.productions)
    assert rsm.start_symbol == ecfg.start_symbol

    for var in ecfg.productions:
        actual = rsm.boxes[var]
        expected = ecfg.productions[var].to_epsilon_nfa()
        assert actual.is_equivalent_to(expected)


def test_minimize_rsm():
    try:
        ecfg = ECFG.ecfg_from_file("tests/test_files/ecfg_1.txt")
    except OSError:
        ecfg = ECFG.ecfg_from_file("test_files/ecfg_1.txt")
    rsm = RSM.rsm_from_ecfg(ecfg)

    assert all(
        rsm.minimize().boxes[var] == create_dfa_by_regex(ecfg.productions[var])
        for var in ecfg.productions.keys()
    )
