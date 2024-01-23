from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser


def test_var_1():
    inp = "x = 5; y = x;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert visitor.scopes[0] == {"x": 5, "y": 5}


def test_var_2():
    inp = """x = "string"; y = x;"""
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert visitor.scopes[0] == {"x": "string", "y": "string"}


def test_var_3():
    inp = "x = true; y = x;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert visitor.scopes[0] == {"x": True, "y": True}
