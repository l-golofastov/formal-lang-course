from pyformlang.cfg import Terminal
from project.context_free.cfg import *


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

    while algorithm_queue:
        variable_queue, start_queue, final_queue = algorithm_queue.pop()
        new_transitions = set()

        for variable_reach, start_reach, final_reach in reachability:

            if final_reach == start_queue:
                for production in wcnf.productions:
                    if (
                        production.body == [variable_reach, variable_queue]
                        and (production.head, start_reach, final_queue)
                        not in reachability
                    ):
                        new_transitions.add((production.head, start_reach, final_queue))

            if final_queue == start_reach:
                for production in wcnf.productions:
                    if (
                        production.body == [variable_queue, variable_reach]
                        and (production.head, start_queue, final_reach)
                        not in reachability
                    ):
                        new_transitions.add((production.head, start_queue, final_reach))

        reachability |= new_transitions
        algorithm_queue |= new_transitions

    return reachability
