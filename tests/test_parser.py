import filecmp
import os
from project.gql.parser import *


def test_accepts_print():
    inp_true = "print (expr);"
    inp_false = "print .not_expr;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False


def test_accepts_var():
    inp_true = "good_variable = true;"
    inp_false = "1_bad_variable = false;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False


def test_accepts_val():
    inp_true = "good_value = 42;"
    inp_false = "bad_value = 0123456789;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False


def test_accepts_vertices():
    inp_get_start_true = "starts = get_start (var);"
    inp_get_start_false = "starts_bad = get_start (.not_var);"
    inp_get_final_true = "finals = get_final (graph);"
    inp_get_reachable_true = "reachables = get_reachable (graph);"
    inp_get_vertices_true = "vertices = get_vertices (graph);"
    inp_edge_true = 'edge = {(0, "label", 1)};'

    assert accepts(inp_get_start_true) == True
    assert accepts(inp_get_start_false) == False
    assert accepts(inp_get_final_true) == True
    assert accepts(inp_get_reachable_true) == True
    assert accepts(inp_get_vertices_true) == True
    assert accepts(inp_edge_true) == True


def test_accepts_labels():
    inp_get_labels_true = "labels = get_labels (var);"
    inp_get_labels_false = "labels_bad = get_labels (.not_var);"
    inp_label_true = "label = {label1};"

    assert accepts(inp_get_labels_true) == True
    assert accepts(inp_get_labels_false) == False
    assert accepts(inp_label_true) == True


def test_accepts_edges():
    inp_get_edges_true = "edges = get_edges (var);"
    inp_get_edges_false = "edges_bad = get_edges (.not_var);"

    assert accepts(inp_get_edges_true) == True
    assert accepts(inp_get_edges_false) == False


def test_accepts_map():
    inp_map_true = "x = map (fun (var) {1}, expr);"
    inp_map_false = "x_bad = map (fun () {}, expr);"

    assert accepts(inp_map_true) == True
    assert accepts(inp_map_false) == False


def test_accepts_filter():
    inp_filter_true = "x = filter (fun (var) {1}, expr);"
    inp_filter_false = "x_bad = filter (fun () {}, expr);"

    assert accepts(inp_filter_true) == True
    assert accepts(inp_filter_false) == False


def test_accepts_intersect():
    inp_intersect_true = 'inter_var = intersect (intersect ("a", 1), "A");'
    inp_intersect_false = "inter_var_bad = intersect (expr);"

    assert accepts(inp_intersect_true) == True
    assert accepts(inp_intersect_false) == False


def test_accepts_concat():
    inp_concat_true = 'x = concat (concat ("a", 1), "A");'
    inp_concat_false = "x_bad = concat (expr);"

    assert accepts(inp_concat_true) == True
    assert accepts(inp_concat_false) == False


def test_accepts_union():
    inp_union_true = 'x = union (union ("a", 1), "A");'
    inp_union_false = "x_bad = union (expr);"

    assert accepts(inp_union_true) == True
    assert accepts(inp_union_false) == False


def test_accepts_star():
    inp_star_true = "starring = (union (expr1, expr2))*;"
    inp_star_false = "starring_bad = (expr1, expr2)*;"

    assert accepts(inp_star_true) == True
    assert accepts(inp_star_false) == False


def test_accepts_comment():
    inp_comment_true = "x = 5; /*comment*/"
    inp_comment_false = "x = 5 ; /*comment"

    assert accepts(inp_comment_true) == True
    assert accepts(inp_comment_false) == False


def test_save_as_dot():
    text = """a = 5;"""
    try:
        save_as_dot(text, "tests/test_files/tree_temp.dot")
        cmp_result = filecmp.cmp(
            "tests/test_files/tree_temp.dot",
            "tests/test_files/tree_expected_1.dot",
            shallow=False,
        )
        os.remove("tests/test_files/tree_temp.dot")
    except OSError:
        save_as_dot(text, "test_files/tree_temp.dot")
        cmp_result = filecmp.cmp(
            "test_files/tree_temp.dot", "test_files/tree_expected_1.dot", shallow=False
        )
        os.remove("test_files/tree_temp.dot")

    assert cmp_result == True
