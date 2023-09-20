import pytest
import cfpq_data
import pydot
import os
import networkx
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


def test_get_dfa_by_regex_determinism():
    dfa = work_with_graph.get_dfa_by_regex("abc|d")

    assert dfa.is_deterministic()


def test_get_dfa_by_regex():
    dfa = work_with_graph.get_dfa_by_regex("abc|d")

    assert dfa.accepts(["abc"])


def test_get_nfa_by_graph_without_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = work_with_graph.get_nfa_by_graph(bzip)

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])


def test_get_nfa_by_graph_with_start_final_nodes_created_by_download():
    bzip_path = cfpq_data.download("bzip")
    bzip = cfpq_data.graph_from_csv(bzip_path)

    nfa = work_with_graph.get_nfa_by_graph(bzip, [223, 102], [257, 422])

    assert nfa.accepts(["d"])
    assert nfa.accepts(["a", "a"])
    assert not nfa.accepts(["d", "a"])


def test_get_nfa_by_graph_without_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = work_with_graph.get_nfa_by_graph(graph)

    assert nfa.accepts(["a"])
    assert nfa.accepts(["b", "a"])
    assert nfa.accepts(["a", "b"])


def test_get_nfa_by_graph_with_start_final_nodes_created_by_function():
    graph = cfpq_data.labeled_two_cycles_graph(3, 4, labels=("a", "b"))

    nfa = work_with_graph.get_nfa_by_graph(graph, [6], [1])

    assert not nfa.accepts(["b", "a"])
    assert nfa.accepts(["b", "b", "a"])
    assert not nfa.accepts(["a", "b"])
