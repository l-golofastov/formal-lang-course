from pyformlang.cfg.cfg import Variable
from project.context_free.hellings import *


def cfpq(
    grammar,
    graph,
    start_nodes=None,
    final_nodes=None,
    start_variable=None,
    algorithm=hellings,
):
    result = set()

    start_nodes = start_nodes if start_nodes is not None else graph.nodes
    final_nodes = final_nodes if final_nodes is not None else graph.nodes
    start_variable = (
        start_variable
        if start_variable is not None
        else (
            grammar.start_symbol if grammar.start_symbol is not None else Variable("S")
        )
    )
    triplets = algorithm(grammar, graph)

    for variable_triplet, start_triplet, final_triplet in triplets:
        for start_input in start_nodes:
            for final_input in final_nodes:
                if (
                    variable_triplet == start_variable
                    and start_triplet == start_input
                    and final_triplet == final_input
                ):
                    result.add((start_triplet, final_triplet))

    return result
