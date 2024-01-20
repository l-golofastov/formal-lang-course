from pathlib import Path

from antlr4 import InputStream, CommonTokenStream, ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl, ParseTreeWalker
from pydot import Dot, Edge, Node

from project.gql.GQLLexer import GQLLexer
from project.gql.GQLListener import GQLListener
from project.gql.GQLParser import GQLParser


def get_parser(inp):
    input_stream = InputStream(inp)
    lexer = GQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    return GQLParser(stream)


def accepts(inp):
    """
    Checks if the input belongs to the language.

    Parameters
    ----------
    inp: str
        The input.

    Returns
    -------
    res: bool
        True or False.
    """
    parser = get_parser(inp)
    parser.removeErrorListeners()
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def save_as_dot(inp, file):
    """
    Generates a description of the parse tree for a given input to a given file in DOT format.

    Parameters
    ----------
    inp: str
        The input.
    file: Path | str
        Path to the file.
    """
    if not accepts(inp):
        raise ValueError("The input does not belong to the language.")
    parser = get_parser(inp)
    listener = DotTreeListener()
    ParseTreeWalker().walk(listener, parser.prog())
    listener.dot.write(str(file))


class DotTreeListener(GQLListener):
    def __init__(self):
        self.dot = Dot("tree", graph_type="digraph")
        self.num_nodes = 0
        self.nodes = {}
        self.rules = GQLParser.ruleNames
        super(DotTreeListener, self).__init__()

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self.nodes:
            self.num_nodes += 1
            self.nodes[ctx] = self.num_nodes
        if ctx.parentCtx:
            self.dot.add_edge(Edge(self.nodes[ctx.parentCtx], self.nodes[ctx]))
        label = self.rules[ctx.getRuleIndex()]
        self.dot.add_node(Node(self.nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self.num_nodes += 1
        self.dot.add_edge(Edge(self.nodes[node.parentCtx], self.num_nodes))
        self.dot.add_node(Node(self.num_nodes, label=f"{node.getText()}"))
