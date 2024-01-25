import pytest

from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph, get_nodes_edges_labels


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        x = get_labels(x);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        x = get_labels(x);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        x = get_labels(x);
        """,
            "wc",
        ),
    ],
)
def test_get_labels(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("x")
    gr = get_graph(graph)
    expected = get_nodes_edges_labels(gr)[2]

    assert labels == expected


@pytest.mark.parametrize(
    "inp, res",
    [
        (
            """
        x = "label";
        y = {x, 1, "another_label"};
        """,
            {"label", "1", "another_label"},
        ),
        (
            """
        y = {1, 2, 3, "labels"};
        """,
            {"1", "2", "3", "labels"},
        ),
    ],
)
def test_labels(inp, res):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("y")

    assert labels == res
