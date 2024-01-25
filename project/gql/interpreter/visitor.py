import sys
from typing import Set

from pyformlang.finite_automaton import (
    State,
    NondeterministicFiniteAutomaton,
    EpsilonNFA,
)
from project.gql.GQLParser import GQLParser
from project.gql.GQLVisitor import GQLVisitor
from project.gql.interpreter.exceptions import *
from project.regular.graph_utils import get_graph
from project.regular.graph_utils import create_nfa_by_graph
from project.regular.regular_path_query import rpq_for_interpreter


class Visitor(GQLVisitor):
    def __init__(self):
        self.scopes = [{}]

    def add_variable(self, name, value):
        self.scopes[-1][name] = value

    def find_variable(self, name):
        level = len(self.scopes) - 1
        while level >= 0:
            if name in self.scopes[level]:
                return self.scopes[level].get(name)
            level = level - 1
        raise UnknownVariableException(name)

    def add_scope(self):
        new_scope = dict()
        self.scopes.append(new_scope)

    def remove_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()
        else:
            raise RemoveGlobalScopeException()

    def visitStmt(self, ctx: GQLParser.StmtContext):
        if ctx.var():
            name = ctx.var().ID_CHAR().getText()
            for i in ctx.var().string().getChildren():
                name = name + str(i)
            value = self.visit(ctx.expr())
            self.add_variable(name=name, value=value)
        else:
            value = self.visit(ctx.expr())
            sys.stdout.write(str(value) + "\n")

    def visitVar(self, ctx: GQLParser.VarContext):
        name = ctx.ID_CHAR().getText()
        for i in ctx.string().getChildren():
            name += str(i)
        return self.find_variable(name=name)

    def visitVal(self, ctx: GQLParser.ValContext):
        if ctx.INT():
            return int(ctx.INT().getText())
        elif ctx.BOOL():
            return bool(ctx.BOOL().getText())
        elif ctx.string():
            return self.visit(ctx.string())
        elif ctx.graph():
            return self.visit(ctx.graph())
        elif ctx.vertices():
            return self.visit(ctx.vertices())
        elif ctx.labels():
            return self.visit(ctx.labels())
        elif ctx.edges():
            return self.visit(ctx.edges())
        else:
            return self.visitChildren(ctx)

    def visitString(self, ctx: GQLParser.StringContext):
        string = ""
        for i in ctx.getChildren():
            string += str(i)
        return string

    def visitGraph(self, ctx: GQLParser.GraphContext):
        if ctx.var():
            x = self.visit(ctx.var())
            if isinstance(x, NondeterministicFiniteAutomaton) | isinstance(
                x, EpsilonNFA
            ):
                return x
            else:
                raise TypeException(
                    expected="NondeterministicFiniteAutomaton", actual=str(type(x))
                )
        elif ctx.getChild(0).getText() == "load_graph":
            return self.visit(ctx.path())
        elif ctx.getChild(0).getText() == "set_start":
            vertices = self.visit(ctx.vertices())
            graph = self.visit(ctx.graph())
            new_graph = graph.copy()
            old_start_states = graph.start_states
            for state in old_start_states:
                new_graph.remove_start_state(state)
            for vertex in vertices:
                new_graph.add_start_state(State(vertex))
            return new_graph
        elif ctx.getChild(0).getText() == "set_final":
            vertices = self.visit(ctx.vertices())
            graph = self.visit(ctx.graph())
            new_graph = graph.copy()
            old_final_states = graph.final_states
            for state in old_final_states:
                new_graph.remove_final_state(state)
            for vertex in vertices:
                new_graph.add_final_state(State(vertex))
            return new_graph
        elif ctx.getChild(0).getText() == "add_start":
            vertices = self.visit(ctx.vertices())
            graph = self.visit(ctx.graph())
            for vertex in vertices:
                graph.add_start_state(State(vertex))
            return graph
        elif ctx.getChild(0).getText() == "add_final":
            vertices = self.visit(ctx.vertices())
            graph = self.visit(ctx.graph())
            for vertex in vertices:
                graph.add_final_state(State(vertex))
            return graph
        else:
            return self.visitChildren(ctx)

    def visitPath(self, ctx: GQLParser.PathContext):
        if ctx.var():
            return self.visit(ctx.var)
        else:
            name = self.visit(ctx.string())
            try:
                return create_nfa_by_graph(
                    graph=get_graph(name), start_nodes=set(), final_nodes=set()
                )
            except:
                raise LoadGraphException(name)

    def visitVertices(self, ctx: GQLParser.VerticesContext):
        if ctx.var():
            x = self.visit((ctx.var()))
            if isinstance(x, Set):
                return x
            else:
                raise TypeException(expected="Set", actual=str(type(x)))
        elif ctx.EMPTY_SET():
            return set()
        elif ctx.INT():
            vertices = set()
            for v in ctx.INT():
                vertices.add(int(str(v)))
            return vertices
        elif ctx.getChild(0).getText() == "get_start":
            return self.visit(ctx.graph()).start_states
        elif ctx.getChild(0).getText() == "get_final":
            return self.visit(ctx.graph()).final_states
        elif ctx.getChild(0).getText() == "get_reachable":
            graph = self.visit(ctx.graph())
            return rpq_for_interpreter(graph)
        elif ctx.getChild(0).getText() == "get_vertices":
            return self.visit(ctx.graph()).states
        else:
            return self.visitChildren(ctx)

    def visitLabels(self, ctx: GQLParser.LabelsContext):
        if ctx.graph():
            graph = self.visit(ctx.graph())
            return graph.symbols
        elif ctx.EMPTY_SET():
            return set()
        elif ctx.getChild(0).getText() == "{":
            labs = set()
            for i in ctx.INT():
                labs.add(str(i))
            for i in ctx.string():
                labs.add(self.visit(i))
            for i in ctx.var():
                labs.add(self.visit(i))
            return labs
        else:
            return self.visitChildren(ctx)

    def visitEdges(self, ctx: GQLParser.EdgesContext):
        if ctx.graph():
            graph = self.visit(ctx.graph())
            return set(graph.to_networkx().edges)
        elif ctx.EMPTY_SET():
            return set()
        else:
            return self.visitChildren(ctx)

    def visitLambda(self, ctx: GQLParser.LambdaContext):
        return self.visitChildren(ctx)

    def visitMap(self, ctx: GQLParser.MapContext):
        return self.visitChildren(ctx)

    def visitFilter(self, ctx: GQLParser.FilterContext):
        return self.visitChildren(ctx)
