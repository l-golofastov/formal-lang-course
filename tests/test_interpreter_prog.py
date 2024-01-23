from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser


def test_prog_1():
    inp = ""
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {}


def test_prog_2():
    inp = "x = 5;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"x": 5}


def test_prog_3():
    inp = "x = true;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"x": True}


def test_prog_4():
    inp = """x = "string"; """
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"x": "string"}


def test_prog_5():
    inp = "x /*comment*/ = 5;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"x": 5}


def test_prog_6():
    inp = "name_of_variable_with_underscore_character = 5;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"name_of_variable_with_underscore_character": 5}


def test_prog_7():
    inp = "name_of_variable_with_int1234 = 5;"
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == {"name_of_variable_with_int1234": 5}
