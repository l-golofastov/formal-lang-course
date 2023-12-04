from cfpq_data import labeled_two_cycles_graph, labeled_cycle_graph
from networkx import MultiDiGraph
from project.context_free.cfpq import *
from project.context_free.hellings import *


def test_cfpq_hellings_1():
    grammar = CFG.from_text(
        """
        S -> A B
        S -> $
        S1 -> S B
        A -> a
        S -> S1
        B -> b
    """
    )
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))
    expected = {(0, 4), (2, 2)}

    assert cfpq(grammar, graph, {0, 2}, {2, 4}, Variable("S"), hellings) == expected


def test_cfpq_hellings_2():
    grammar = CFG.from_text(
        """
        S -> A B | A S1
        S1 -> S B
        A -> a
        B -> b
    """
    )
    graph = MultiDiGraph()
    graph.add_nodes_from([0, 1, 2, 3])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 0, label="a")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 2, label="b")

    assert cfpq(grammar, graph, {0, 1}, {1, 2, 3}, algorithm=hellings) == {
        (0, 2),
        (1, 3),
        (1, 2),
        (0, 3),
    }


def test_cfpq_hellings_3():
    grammar = CFG.from_text(
        """
        S -> a | $
    """
    )
    graph = labeled_cycle_graph(3, "a")

    assert cfpq(grammar, graph, {0}, {0, 1}, Variable("S"), hellings) == {
        (0, 0),
        (0, 1),
    }


def test_cfpq_hellings_4():
    grammar = CFG.from_text(
        """
        S -> A B
        S -> A C
        C -> S B
        A -> a
        B -> b
    """
    )
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))

    assert cfpq(grammar, graph, None, None, Variable("S"), hellings) == {
        (3, 4),
        (2, 5),
        (1, 0),
        (0, 4),
        (3, 5),
        (2, 0),
        (1, 4),
        (0, 5),
        (3, 0),
        (2, 4),
        (1, 5),
        (0, 0),
    }


def test_cfpq_hellings_5():
    grammar = CFG.from_text(
        """
        S -> $
    """
    )
    graph = labeled_two_cycles_graph(3, 2, labels=("a", "b"))

    assert cfpq(grammar, graph, {0}, {1, 2, 4}, Variable("S"), hellings) == set()
