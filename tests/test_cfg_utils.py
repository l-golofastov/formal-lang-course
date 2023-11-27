import pytest

from project.cfg import *


def test_cfg_to_wcnf_decompose_productions():
    cfg = CFG.from_text(
        """
		S -> A B C
		A -> a
		B -> b
		C -> c
	"""
    )

    cfg_wcnf = cfg_to_wcnf(cfg)
    try:
        expected_cfg = read_cfg_from_file("tests/test_files/wcnf_1.txt")
    except OSError:
        expected_cfg = read_cfg_from_file("test_files/wcnf_1.txt")

    assert cfg_wcnf.start_symbol == expected_cfg.start_symbol
    assert cfg_wcnf.terminals == expected_cfg.terminals
    assert cfg_wcnf.variables == expected_cfg.variables
    assert cfg_wcnf.productions == expected_cfg.productions


def test_cfg_to_wcnf_remove_useless_symbols():
    cfg = CFG.from_text(
        """
		S -> A B C
		A -> a
		B -> b
		C -> c
		N -> $
	"""
    )

    cfg_wcnf = cfg_to_wcnf(cfg)
    try:
        expected_cfg = read_cfg_from_file("tests/test_files/wcnf_1.txt")
    except OSError:
        expected_cfg = read_cfg_from_file("test_files/wcnf_1.txt")

    assert cfg_wcnf.start_symbol == expected_cfg.start_symbol
    assert cfg_wcnf.terminals == expected_cfg.terminals
    assert cfg_wcnf.variables == expected_cfg.variables
    assert cfg_wcnf.productions == expected_cfg.productions


def test_cfg_to_wcnf_eliminate_unit_productions():
    cfg = CFG.from_text(
        """
		S -> A B C X
		A -> a
		B -> b
		C -> c
		X -> Y
		Y -> x
		N -> $
	"""
    )

    cfg_wcnf = cfg_to_wcnf(cfg)
    try:
        expected_cfg = read_cfg_from_file("tests/test_files/wcnf_2.txt")
    except OSError:
        expected_cfg = read_cfg_from_file("test_files/wcnf_2.txt")

    assert cfg_wcnf.start_symbol == expected_cfg.start_symbol
    assert cfg_wcnf.terminals == expected_cfg.terminals
    assert cfg_wcnf.variables == expected_cfg.variables
    assert cfg_wcnf.productions == expected_cfg.productions


def test_cfg_to_wcnf_delete_multiple_terminals():
    cfg = CFG.from_text(
        """
		S -> A B
		A -> a aa aalanguage
		B -> b
		N -> $
	"""
    )

    cfg_wcnf = cfg_to_wcnf(cfg)
    try:
        expected_cfg = read_cfg_from_file("tests/test_files/wcnf_3.txt")
    except OSError:
        expected_cfg = read_cfg_from_file("test_files/wcnf_3.txt")

    assert cfg_wcnf.start_symbol == expected_cfg.start_symbol
    assert cfg_wcnf.terminals == expected_cfg.terminals
    assert cfg_wcnf.variables == expected_cfg.variables
    assert cfg_wcnf.productions == expected_cfg.productions


def test_cfg_to_wcnf_empty():
    try:
        cfg = read_cfg_from_file("tests/test_files/wcnf_4.txt")
    except OSError:
        cfg = read_cfg_from_file("test_files/wcnf_4.txt")

    assert cfg.is_empty()
