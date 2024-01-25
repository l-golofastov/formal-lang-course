import pytest

from project.gql.interpreter.visitor import Visitor
from project.gql.parser import get_parser


@pytest.mark.parametrize(
    "inp, res",
    [
        ("x = 5; y = x;", {"x": 5, "y": 5}),
        ("""x = "string"; y = x;""", {"x": "string", "y": "string"}),
        ("x = true; y = x;", {"x": True, "y": True}),
    ],
)
def test_var(inp, res):
    ctx = get_parser(inp).prog()
    visitor = Visitor()
    visitor.visitProg(ctx)

    assert visitor.scopes[0] == res
