import pytest

from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph


def check_graph_and_nfa(expected_graph, actual_nfa, start_states=0, final_states=0):
    assert len(actual_nfa.states) == expected_graph.number_of_nodes()
    assert actual_nfa.get_number_transitions() == expected_graph.number_of_edges()
    assert len(actual_nfa.start_states) == start_states
    assert len(actual_nfa.final_states) == final_states


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
         x = load_graph("skos");
          """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        """,
            "wc",
        ),
    ],
)
def test_load_graph(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph(graph)
    actual_nfa = visitor.scopes[0].get("x")
    check_graph_and_nfa(expected_graph, actual_nfa)


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        y = add_start({0, 1, 2}, x);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        y = add_start({0, 1, 2}, x);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        y = add_start({0, 1, 2}, x);
        """,
            "wc",
        ),
    ],
)
def test_add_start(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph(graph)
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=3)


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        y = add_final({0, 1, 2}, x);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        y = add_final({0, 1, 2}, x);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        y = add_final({0, 1, 2}, x);
        """,
            "wc",
        ),
    ],
)
def test_add_final(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph(graph)
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=3)


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """,
            "wc",
        ),
    ],
)
def test_set_start(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph(graph)
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=1)


@pytest.mark.parametrize(
    "inp, graph",
    [
        (
            """
        x = load_graph("skos");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """,
            "skos",
        ),
        (
            """
        x = load_graph("atom");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """,
            "atom",
        ),
        (
            """
        x = load_graph("wc");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """,
            "wc",
        ),
    ],
)
def test_set_final(inp, graph):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph(graph)
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=1)
