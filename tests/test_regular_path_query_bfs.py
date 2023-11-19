import pytest

from project.regular_path_query import *
from pyformlang.finite_automaton.nondeterministic_finite_automaton import *
from networkx import MultiDiGraph
from cfpq_data import *


def test_rpq_bfs_empty():
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))

    assert rpq_bfs("(c|d)*", graph) == set()
    assert rpq_bfs("(c|d)*", graph, option=True) == {
        0: set(),
        1: set(),
        2: set(),
        3: set(),
        4: set(),
        5: set(),
        6: set(),
    }


def test_rpq_bfs_no_cycles_graph():
    graph = networkx.MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (0, 2, {"label": "c"}),
            (0, 3, {"label": "b"}),
            (3, 4, {"label": "aa"}),
        ]
    )

    assert rpq_bfs("(a|b)(aa)*", graph, [0]) == {1, 3, 4}


def test_rpq_bfs_cycled_graph():
    graph = MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (1, 2, {"label": "b"}),
            (2, 3, {"label": "a"}),
            (3, 4, {"label": "b"}),
            (0, 2, {"label": "a"}),
            (2, 5, {"label": "b"}),
            (3, 6, {"label": "a"}),
            (6, 0, {"label": "b"}),
        ]
    )

    assert rpq_bfs("(a|b)*", graph) == {0, 1, 2, 3, 4, 5, 6}


def test_rpq_bfs_all_1():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(0), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    graph = automaton.to_networkx()

    assert rpq_bfs("(a|f).(b|d)", graph, {0}, {2, 4}) == {2}


def test_rpq_bfs_all_2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("d"), State(1))
    automaton.add_transition(State(1), Symbol("c"), State(2))
    automaton.add_transition(State(2), Symbol("c"), State(4))
    automaton.add_transition(State(1), Symbol("a"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(0), Symbol("c"), State(5))
    graph = automaton.to_networkx()

    assert rpq_bfs("(c*|d).(c*)", graph, {0}) == {1, 2, 4, 5}


def test_rpq_bfs_all_3():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("b"), State(2))
    automaton.add_transition(State(1), Symbol("d"), State(3))
    automaton.add_transition(State(0), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("d"), State(5))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(0), Symbol("a"), State(9))
    automaton.add_transition(State(9), Symbol("a"), State(7))
    automaton.add_transition(State(9), Symbol("b"), State(8))
    automaton.add_transition(State(7), Symbol("b"), State(6))
    graph = automaton.to_networkx()

    assert rpq_bfs("a.b", graph, {0, 9}) == {2, 6, 8}


def test_rpq_bfs_for_each_1():
    graph = MultiDiGraph()
    graph.add_edges_from(
        [
            (0, 1, {"label": "a"}),
            (0, 2, {"label": "b"}),
            (1, 2, {"label": "b"}),
            (2, 2, {"label": "c"}),
        ]
    )

    assert rpq_bfs("a.b*", graph, [0, 1], [2], True) == {0: {2}, 1: set()}


def test_rpq_bfs_for_each_2():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(2))
    automaton.add_transition(State(1), Symbol("b"), State(3))
    automaton.add_transition(State(2), Symbol("b"), State(3))
    automaton.add_transition(State(3), Symbol("c"), State(4))
    automaton.add_transition(State(4), Symbol("c"), State(7))
    automaton.add_transition(State(4), Symbol("d"), State(6))
    automaton.add_transition(State(5), Symbol("e"), State(6))
    automaton.add_transition(State(7), Symbol("e"), State(6))
    graph = automaton.to_networkx()

    assert rpq_bfs("(a*).(b*).(c*).(e*)", graph, {0, 4}, option=True) == {
        0: {1, 2, 3, 4, 7, 6},
        4: {6, 7},
    }


def test_rpq_bfs_for_each_3():
    graph = labeled_two_cycles_graph(3, 3, labels=("a", "b"))

    assert rpq_bfs("(a*|b)", graph, [0, 2], [1, 2, 3], option=True) == {
        0: {1, 2, 3},
        2: {1, 2, 3},
    }


def test_rpq_bfs_for_each_all():
    graph = MultiDiGraph()
    nodes = [0, 1, 2, 3]
    edges = [(0, 1, {"label": "a"}), (1, 2, {"label": "b"}), (2, 3, {"label": "c"})]
    graph.add_nodes_from(nodes)
    graph.add_edges_from(edges)

    assert rpq_bfs("a|c", graph, [0], [1, 2, 3], option=True) == {0: {1}}
    assert rpq_bfs("a|c", graph, [0, 2], [1, 2, 3], option=True) == {0: {1}, 2: {3}}
    assert rpq_bfs("a|c", graph, [0, 2], [1, 2, 3]) == {1, 3}
