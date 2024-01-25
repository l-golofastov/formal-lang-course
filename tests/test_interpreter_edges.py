import pytest

from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        x = get_edges(x);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        x = get_edges(x);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        x = get_edges(x);
        """,
            "wc",
        ),
    ],
)
def test_get_edges(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    edges = visitor.scopes[0].get("x")
    expected = set(get_graph(graph).edges)

    assert edges == expected
