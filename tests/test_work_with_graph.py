import pytest
import cfpq_data
import pydot
import os
import networkx
import pyformlang
import scipy
from project import work_with_graph


def test_get_nodes_edges_labels_created_graph():
    graph = cfpq_data.labeled_cycle_graph(4, "a")

    assert work_with_graph.get_nodes_edges_labels(graph) == (4, 4, {"a"})


def test_get_nodes_edges_labels_downloaded_graph():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    assert work_with_graph.get_nodes_edges_labels(bzip)[0] == 632
    assert work_with_graph.get_nodes_edges_labels(bzip)[1] == 556
    assert True == (
        work_with_graph.get_nodes_edges_labels(bzip)[2] == {"a", "d"}
        or work_with_graph.get_nodes_edges_labels(bzip)[2] == {"d", "a"}
    )


def test_save_two_cycles_graph_file_existing():
    work_with_graph.save_two_cycles_graph(
        3, 4, ("a", "b"), "save_two_cycles_graph_output.dot"
    )

    assert os.path.exists("save_two_cycles_graph_output.dot")

    os.remove("save_two_cycles_graph_output.dot")


def test_save_two_cycles_graph_save_correction():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    work_with_graph.save_two_cycles_graph(
        3, 4, ("a", "b"), "save_two_cycles_graph_output.dot"
    )
    saved_graph = pydot.graph_from_dot_file("save_two_cycles_graph_output.dot")

    pydot_graph_raw = (
        networkx.drawing.nx_pydot.to_pydot(graph).to_string().splitlines()[1:-1]
    )
    saved_graph_raw = saved_graph[0].to_string().splitlines()[1:-2]

    for i in range(len(pydot_graph_raw)):
        pydot_graph_line = pydot_graph_raw[i]
        saved_graph_line = saved_graph_raw[i]
        assert pydot_graph_line == saved_graph_line

    os.remove("save_two_cycles_graph_output.dot")


def test_create_dfa_by_regex_determinism():
    dfa = work_with_graph.create_dfa_by_regex("abc|d")

    assert dfa.is_deterministic()


def test_create_dfa_by_regex_acceptance():
    dfa = work_with_graph.create_dfa_by_regex("abc|d")

    assert dfa.accepts(["abc"])


def test_create_nfa_by_graph_without_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = work_with_graph.create_nfa_by_graph(bzip)

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])


def test_create_nfa_by_graph_with_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = work_with_graph.create_nfa_by_graph(bzip, [223, 102], [257, 422])

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])
    assert not nfa.accepts(["d", "a"])


def test_create_nfa_by_graph_without_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = work_with_graph.create_nfa_by_graph(graph)

    assert nfa.accepts(["a"])
    assert nfa.accepts(["b", "a"])
    assert nfa.accepts(["a", "b"])


def test_create_nfa_by_graph_with_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = work_with_graph.create_nfa_by_graph(graph, [6], [1])

    assert not nfa.accepts(["b", "a"])
    assert nfa.accepts(["b", "b", "a"])
    assert not nfa.accepts(["a", "b"])


def test_functionality():

    nfa = pyformlang.finite_automaton.NondeterministicFiniteAutomaton()

    nfa.add_transitions(
        [(0, "abc", 1), (0, "abc", 0), (1, "d", 1), (1, "c", 1), (1, "abc", 1)]
    )

    nfa.add_start_state(0)

    nfa.add_final_state(1)

    nfa_dict = nfa.to_dict()

    dfa = work_with_graph.create_dfa_by_regex("abc|d")
    assert dfa.accepts(["abc"])

    print(dfa.to_dict())

    print(dfa.start_states)
    print(dfa.final_states)

    intersect = work_with_graph.intersect_two_fa(dfa, nfa)

    print(nfa_dict)

    labels_with_nodes = nfa_dict.values()

    # print(list(labels_with_nodes))

    labels = []
    for dict in labels_with_nodes:
        for label in dict.keys():
            labels.append(label)

    # print(list(set(labels)))

    # print(nfa_dict[0]['abc'])

    nfa_new = pyformlang.finite_automaton.NondeterministicFiniteAutomaton()

    nfa_new.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 2), (1, "b", 1)])

    nfa_new.add_start_state(0)

    nfa_new.add_final_state(1)

    matrices = work_with_graph.create_binary_sparse_matrices(dfa)
    for matrix in matrices.values():
        print(matrix.toarray())

    for matrix in intersect.values():
        print(matrix.toarray())

    nfa_new_binary = work_with_graph.create_binary_sparse_matrices(nfa_new)
    nfa_new_closure = work_with_graph.get_transitive_closure(nfa_new_binary)
    intersect_closure = work_with_graph.get_transitive_closure(intersect)
    start_final_states = work_with_graph.get_start_final_states_intersected(dfa, nfa)
    for state in start_final_states['start']:
        print(state)
    for state in start_final_states['final']:
        print(state)

    result = set()
    for pair in intersect_closure:
        start = pair[0]
        final = pair[1]
        if start in start_final_states['start'] and final in start_final_states['final']:
            result_start = pair[0] // len(nfa.states)
            result_final = pair[1] // len(nfa.states)
            result.add((result_start, result_final))
    print(result)
    print()



    for pair in intersect_closure:
        print(pair)

    start_final_states_intersected = work_with_graph.get_start_final_states_intersected(
        dfa, nfa
    )

    print(start_final_states_intersected['start'])
    print(start_final_states_intersected['final'])

    assert True

def test_regular_path_query_1():
    graph_ex = cfpq_data.labeled_two_cycles_graph(2, 2, labels=("a", "b"))
    print(graph_ex.edges(data=True))
    result = work_with_graph.make_regular_path_query("(a + b)* b (a + b)*", graph_ex, [0, 1], [2, 3])
    print(result)
    dfa = work_with_graph.create_dfa_by_regex("(a + b)* b (a + b)*")
    nfa = pyformlang.finite_automaton.NondeterministicFiniteAutomaton()

    nfa.add_transitions([(0, "a", 1), (1, "a", 2), (2, "a", 0), (0, "b", 3), (3, "b", 4), (4, "b", 0)])

    nfa.add_start_state(0)
    nfa.add_start_state(1)
    nfa.add_final_state(2)
    nfa.add_final_state(3)

    intersect = work_with_graph.intersect_two_fa(dfa, nfa)
    transitive = work_with_graph.get_transitive_closure(intersect)
    for pair in transitive:
        print(pair)

    assert dfa.accepts("aba")
    #assert result == {(1, 2), (0, 2), (0, 3), (1, 3)}