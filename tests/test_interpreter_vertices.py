from pyformlang.regular_expression import Regex
from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph, get_nodes_edges_labels
from project.regular.regular_path_query import rpq_tensor


def test_get_start_1():
    inp = """
        x = load_graph("skos");
        y = get_start(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == set()


def test_get_start_2():
    inp = """
        x = load_graph("skos");
        y = get_start(set_start({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_start_3():
    inp = """
        x = load_graph("atom");
        y = get_start(set_start({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_start_4():
    inp = """
        x = load_graph("atom");
        y = get_start(set_start({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_start_5():
    inp = """
        x = load_graph("wc");
        y = get_start(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == set()


def test_get_start_6():
    inp = """
        x = load_graph("wc");
        y = get_start(set_start({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_final_1():
    inp = """
        x = load_graph("skos");
        y = get_final(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == set()


def test_get_final_2():
    inp = """
        x = load_graph("skos");
        y = get_final(set_final({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_final_3():
    inp = """
        x = load_graph("atom");
        y = get_final(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == set()


def test_get_final_4():
    inp = """
        x = load_graph("atom");
        y = get_final(set_final({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_final_5():
    inp = """
        x = load_graph("wc");
        y = get_final(x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == set()


def test_get_final_6():
    inp = """
        x = load_graph("wc");
        y = get_final(set_final({1, 2, 3}, x));
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("y")

    assert vertices == {1, 2, 3}


def test_get_reachable_1():
    inp = """
        x = load_graph("skos");
        y = set_start({0}, x);
        z = set_final({0}, y);
        w = get_reachable(z);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    graph = get_graph("skos")
    labels = get_nodes_edges_labels(graph)[2]
    regex = "(" + labels.pop()

    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)
    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=graph, start_nodes={0}, final_nodes={0}
    ):
        exp.add(j)

    assert vertices == exp


def test_get_reachable_2():
    inp = """
        x = load_graph("skos");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    graph = get_graph("skos")
    labels = get_nodes_edges_labels(graph)[2]
    regex = "(" + labels.pop()

    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)
    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=graph, start_nodes=None, final_nodes=None
    ):
        exp.add(j)

    assert vertices == exp


def test_get_reachable_3():
    inp = """
        x = load_graph("atom");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    graph = get_graph("atom")
    labels = get_nodes_edges_labels(graph)[2]
    regex = "(" + labels.pop()

    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)
    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=graph, start_nodes=None, final_nodes=None
    ):
        exp.add(j)

    assert vertices == exp


def test_get_reachable_4():
    inp = """
        x = load_graph("wc");
        y = set_start(get_vertices(x), x);
        z = set_final(get_vertices(y), y);
        w = get_reachable(z);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    graph = get_graph("wc")
    labels = get_nodes_edges_labels(graph)[2]
    regex = "(" + labels.pop()

    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)
    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=graph, start_nodes=None, final_nodes=None
    ):
        exp.add(j)

    assert vertices == exp


def test_get_reachable_5():
    inp = """
        x = load_graph("atom");
        y = set_start(set(), x);
        z = set_final(set(), y);
        w = get_reachable(z);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    vertices = visitor.scopes[0].get("w")
    graph = get_graph("atom")
    labels = get_nodes_edges_labels(graph)[2]
    regex = "(" + labels.pop()

    for label in labels:
        regex += "|" + label
    regex += ")*"
    regex = Regex(regex)
    exp = set()
    for (_, j) in rpq_tensor(
        regex=regex, graph=graph, start_nodes=set(), final_nodes=set()
    ):
        exp.add(j)

    assert vertices == exp
