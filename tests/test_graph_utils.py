import cfpq_data
import pydot
import os
import networkx as nx
from project.regular import graph_utils


def test_get_nodes_edges_labels_created_graph():
    graph = cfpq_data.labeled_cycle_graph(4, "a")

    assert graph_utils.get_nodes_edges_labels(graph) == (4, 4, {"a"})


def test_get_nodes_edges_labels_downloaded_graph():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    assert graph_utils.get_nodes_edges_labels(bzip)[0] == 632
    assert graph_utils.get_nodes_edges_labels(bzip)[1] == 556
    assert True == (
        graph_utils.get_nodes_edges_labels(bzip)[2] == {"a", "d"}
        or graph_utils.get_nodes_edges_labels(bzip)[2] == {"d", "a"}
    )


def test_save_two_cycles_graph_file_existing():
    graph_utils.save_two_cycles_graph(
        3, 4, ("a", "b"), "save_two_cycles_graph_output.dot"
    )

    assert os.path.exists("save_two_cycles_graph_output.dot")

    os.remove("save_two_cycles_graph_output.dot")


def test_save_two_cycles_graph_save_correction():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    graph_utils.save_two_cycles_graph(
        3, 4, ("a", "b"), "save_two_cycles_graph_output.dot"
    )
    saved_graph = pydot.graph_from_dot_file("save_two_cycles_graph_output.dot")

    pydot_graph_raw = nx.drawing.nx_pydot.to_pydot(graph).to_string().splitlines()[1:-1]
    saved_graph_raw = saved_graph[0].to_string().splitlines()[1:-1]

    for i in range(len(pydot_graph_raw)):
        pydot_graph_line = pydot_graph_raw[i]
        saved_graph_line = saved_graph_raw[i]
        assert pydot_graph_line == saved_graph_line

    os.remove("save_two_cycles_graph_output.dot")


def test_create_dfa_by_regex_determinism():
    dfa = graph_utils.create_dfa_by_regex("abc|d")

    assert dfa.is_deterministic()


def test_create_dfa_by_regex_acceptance():
    dfa = graph_utils.create_dfa_by_regex("abc|d")

    assert dfa.accepts(["abc"])


def test_create_nfa_by_graph_without_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = graph_utils.create_nfa_by_graph(bzip)

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])


def test_create_nfa_by_graph_with_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = graph_utils.create_nfa_by_graph(bzip, [223, 102], [257, 422])

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])
    assert not nfa.accepts(["d", "a"])


def test_create_nfa_by_graph_without_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = graph_utils.create_nfa_by_graph(graph)

    assert nfa.accepts(["a"])
    assert nfa.accepts(["b", "a"])
    assert nfa.accepts(["a", "b"])


def test_create_nfa_by_graph_with_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = graph_utils.create_nfa_by_graph(graph, [6], [1])

    assert not nfa.accepts(["b", "a"])
    assert nfa.accepts(["b", "b", "a"])
    assert not nfa.accepts(["a", "b"])
