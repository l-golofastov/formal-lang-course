from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph, get_nodes_edges_labels


def test_get_labels_1():
    inp = """
        x = load_graph("skos");
        x = get_labels(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("x")
    graph = get_graph("skos")
    expected = get_nodes_edges_labels(graph)[2]

    assert labels == expected


def test_get_labels_2():
    inp = """
        x = load_graph("atom");
        x = get_labels(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("x")
    graph = get_graph("atom")
    expected = get_nodes_edges_labels(graph)[2]

    assert labels == expected


def test_get_labels_3():
    inp = """
        x = load_graph("wc");
        x = get_labels(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("x")
    graph = get_graph("wc")
    expected = get_nodes_edges_labels(graph)[2]

    assert labels == expected


def test_labels_1():
    inp = """
        x = "label";
        y = {x, 1, "another_label"};
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("y")

    assert labels == {"label", "1", "another_label"}


def test_labels_2():
    inp = """
        y = {1, 2, 3, "labels"};
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    labels = visitor.scopes[0].get("y")

    assert labels == {"1", "2", "3", "labels"}
