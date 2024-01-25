import pytest

from pyformlang.regular_expression import Regex
from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph, get_nodes_edges_labels
from project.regular.regular_path_query import rpq_tensor


@pytest.mark.parametrize(
    "inp, graph, res",
    [
        (
            """
        x = load_graph("skos");
        y = get_start(x);
        """,
            "skos",
            set(),
        ),
        (
            """
        x = load_graph("skos");
        y = get_start(set_start({1, 2, 3}, x));
        """,
            "skos",
            {1, 2, 3},
        ),
        (
            """
        x = load_graph("atom");
        y = get_start(x);
        """,
            "atom",
            set(),
        ),
        (
            """
        x = load_graph("atom");
        y = get_start(set_start({1, 2, 3}, x));
        """,
            "atom",
            {1, 2, 3},
        ),
        (
            """
        x = load_graph("wc");
        y = get_start(x);
        """,
            "wc",
            set(),
        ),
        (
            """
        x = load_graph("wc");
        y = get_start(set_start({1, 2, 3}, x));
        """,
            "wc",
            {1, 2, 3},
        ),
    ],
)
def test_get_start(inp, graph, res):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == res


@pytest.mark.parametrize(
    "inp, graph, res",
    [
        (
            """
        x = load_graph("skos");
        y = get_final(x);
        """,
            "skos",
            set(),
        ),
        (
            """
        x = load_graph("skos");
        y = get_final(set_final({1, 2, 3}, x));
        """,
            "skos",
            {1, 2, 3},
        ),
        (
            """
        x = load_graph("atom");
        y = get_final(x);
        """,
            "atom",
            set(),
        ),
        (
            """
        x = load_graph("atom");
        y = get_final(set_final({1, 2, 3}, x));
        """,
            "atom",
            {1, 2, 3},
        ),
        (
            """
        x = load_graph("wc");
        y = get_final(x);
        """,
            "wc",
            set(),
        ),
        (
            """
        x = load_graph("wc");
        y = get_final(set_final({1, 2, 3}, x));
        """,
            "wc",
            {1, 2, 3},
        ),
    ],
)
def test_get_final(inp, graph, res):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == res


@pytest.mark.parametrize(
    "inp, graph, start, final",
    [
        (
            """
        x = load_graph("skos");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """,
            "skos",
            None,
            None,
        ),
        (
            """
        x = load_graph("skos");
        y = set_start({0}, x);
        z = set_final({0}, y);
        w = get_reachable(z);
        """,
            "skos",
            {0},
            {0},
        ),
        (
            """
        x = load_graph("atom");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """,
            "atom",
            None,
            None,
        ),
        (
            """
        x = load_graph("wc");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """,
            "wc",
            None,
            None,
        ),
        (
            """
        x = load_graph("atom");
        y = set_start(set(), x);
        z = set_final(set(), y);
        w = get_reachable(z);
        """,
            "atom",
            set(),
            set(),
        ),
    ],
)
def test_get_reachable(inp, graph, start, final):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    gr = get_graph(graph)
    labels = get_nodes_edges_labels(gr)[2]

    regex = "(" + labels.pop()
    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)

    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=gr, start_nodes=start, final_nodes=final
    ):
        exp.add(j)

    assert vertices == exp


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        x = get_vertices(x);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        x = get_vertices(x);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        x = get_vertices(x);
        """,
            "wc",
        ),
    ],
)
def test_get_vertices(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("x")
    expected = set(get_graph(graph).nodes)

    assert vertices == expected
