from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph


def test_get_edges_1():
    inp = """
        x = load_graph("skos");
        x = get_edges(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    edges = visitor.scopes[0].get("x")
    expected = set(get_graph("skos").edges)

    assert edges == expected


def test_get_edges_2():
    inp = """
        x = load_graph("atom");
        x = get_edges(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    edges = visitor.scopes[0].get("x")
    expected = set(get_graph("atom").edges)

    assert edges == expected


def test_get_edges_3():
    inp = """
        x = load_graph("wc");
        x = get_edges(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    edges = visitor.scopes[0].get("x")
    expected = set(get_graph("wc").edges)

    assert edges == expected
