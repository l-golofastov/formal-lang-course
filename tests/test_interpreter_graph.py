from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser
from project.regular.graph_utils import get_graph


def check_graph_and_nfa(expected_graph, actual_nfa, start_states=0, final_states=0):
    assert len(actual_nfa.states) == expected_graph.number_of_nodes()
    assert actual_nfa.get_number_transitions() == expected_graph.number_of_edges()
    assert len(actual_nfa.start_states) == start_states
    assert len(actual_nfa.final_states) == final_states


def test_load_graph_1():
    inp = """
         x = load_graph("skos");
          """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("skos")
    actual_nfa = visitor.scopes[0].get("x")
    check_graph_and_nfa(expected_graph, actual_nfa)


def test_load_graph_2():
    inp = """
         x = load_graph("atom");
          """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("atom")
    actual_nfa = visitor.scopes[0].get("x")
    check_graph_and_nfa(expected_graph, actual_nfa)


def test_load_graph_3():
    inp = """
         x = load_graph("wc");
          """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("wc")
    actual_nfa = visitor.scopes[0].get("x")
    check_graph_and_nfa(expected_graph, actual_nfa)


def test_add_start_1():
    inp = """
        x = load_graph("skos");
        y = add_start({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("skos")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=3)


def test_add_start_2():
    inp = """
        x = load_graph("atom");
        y = add_start({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("atom")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=3)


def test_add_start_3():
    inp = """
        x = load_graph("wc");
        y = add_start({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("wc")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=3)


def test_final_1():
    inp = """
        x = load_graph("skos");
        y = add_final({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("skos")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=3)


def test_add_final_2():
    inp = """
        x = load_graph("atom");
        y = add_final({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("atom")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=3)


def test_final_start_3():
    inp = """
        x = load_graph("wc");
        y = add_final({0, 1, 2}, x);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("wc")
    actual_nfa = visitor.scopes[0].get("y")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=3)


def test_set_start_1():
    inp = """
        x = load_graph("skos");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("skos")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=1)


def test_set_start_2():
    inp = """
        x = load_graph("atom");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("atom")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=1)


def test_set_start_3():
    inp = """
        x = load_graph("wc");
        y = add_start({0, 1, 2}, x);
        z = set_start({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("wc")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, start_states=1)


def test_set_final_1():
    inp = """
        x = load_graph("skos");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("skos")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=1)


def test_set_final_2():
    inp = """
        x = load_graph("atom");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("atom")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=1)


def test_set_final_3():
    inp = """
        x = load_graph("wc");
        y = add_final({0, 1, 2}, x);
        z = set_final({0}, y);
        """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)
    expected_graph = get_graph("wc")
    actual_nfa = visitor.scopes[0].get("z")
    check_graph_and_nfa(expected_graph, actual_nfa, final_states=1)
