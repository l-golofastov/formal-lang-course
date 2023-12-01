import cfpq_data
import networkx as nx
from pyformlang.finite_automaton import State, Symbol, NondeterministicFiniteAutomaton
from project.regular import regular_path_query


def test_rpq_tensor_with_empty_graph():
    graph = nx.MultiDiGraph()
    result = regular_path_query.rpq_tensor("", graph)

    assert result == set()


def test_rpq_tensor_with_simple_graph_and_nonempty_intersection():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(0))
    graph = automaton.to_networkx()
    result = regular_path_query.rpq_tensor("a|b", graph)

    assert result == {(0, 1), (1, 0)}


def test_rpq_tensor_with_simple_graph_and_empty_intersection():
    automaton = NondeterministicFiniteAutomaton()
    automaton.add_transition(State(0), Symbol("a"), State(1))
    automaton.add_transition(State(1), Symbol("a"), State(0))
    graph = automaton.to_networkx()
    result = regular_path_query.rpq_tensor("b*", graph)

    assert result == set()


def test_rpq_tensor_labeled_two_cycles_graph():
    graph = cfpq_data.labeled_two_cycles_graph(2, 2, labels=("a", "b"))
    result = regular_path_query.rpq_tensor("(a + b)* b (a + b)*", graph, [0, 1], [2, 3])

    assert result == {(1, 2), (0, 2), (0, 3), (1, 3)}
