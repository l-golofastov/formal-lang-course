from pyformlang.cfg import Terminal
from project.context_free.cfg import *
from project.regular.graph_utils import *


def hellings(grammar, graph):
    wcnf = cfg_to_wcnf(grammar)

    epsilon_variables = {
        production.head for production in wcnf.productions if len(production.body) == 0
    }
    epsilon_transitions = {
        (variable, node, node) for variable in epsilon_variables for node in graph.nodes
    }

    transitions = set()
    for production in wcnf.productions:
        for start, final, label in graph.edges(data="label"):
            if len(production.body) == 1:
                if production.body[0] == Terminal(label):
                    transitions.add((production.head, start, final))

    reachability = epsilon_transitions | transitions
    algorithm_queue = reachability.copy()

    return reachability
