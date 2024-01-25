import pytest

from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser


@pytest.mark.parametrize(
    "inp, res",
    [
        ("", {}),
        ("x = 5;", {"x": 5}),
        ("x = true;", {"x": True}),
        ("""x = "string"; """, {"x": "string"}),
        ("x /*comment*/ = 5;", {"x": 5}),
        (
            "name_of_variable_with_underscore_character = 5;",
            {"name_of_variable_with_underscore_character": 5},
        ),
        ("name_of_variable_with_int1234 = 5;", {"name_of_variable_with_int1234": 5}),
    ],
)
def test_prog_bind(inp, res):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert len(visitor.scopes) == 1
    assert visitor.scopes[0] == res
