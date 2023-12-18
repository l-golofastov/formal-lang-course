from pyformlang.cfg import Terminal
from project.context_free.cfg import *
from scipy.sparse.dok import dok_matrix


def matrix(grammar, graph):
    wcnf = cfg_to_wcnf(grammar)

    decomposed_matrices = {
        variable: dok_matrix((len(graph.nodes), len(graph.nodes)), dtype=int)
        for variable in wcnf.variables
    }

    epsilon_variables = {
        production.head for production in wcnf.productions if len(production.body) == 0
    }

    for variable in epsilon_variables:
        for i in range(len(graph.nodes)):
            decomposed_matrices[variable][i, i] = 1
    for production in wcnf.productions:
        for start, final, label in graph.edges(data="label"):
            if len(production.body) == 1 and production.body[0] == Terminal(label):
                decomposed_matrices[production.head][start, final] = 1

    prev = 0
    curr = sum(
        [
            variable_matrix.count_nonzero()
            for variable_matrix in decomposed_matrices.values()
        ]
    )

    while prev != curr:
        for production in wcnf.productions:
            if len(production.body) == 2:
                start_variable = production.body[0]
                final_variable = production.body[1]
                decomposed_matrices[production.head] += (
                    decomposed_matrices[start_variable]
                    @ decomposed_matrices[final_variable]
                )

        prev = curr
        curr = sum(
            [
                variable_matrix.count_nonzero()
                for variable_matrix in decomposed_matrices.values()
            ]
        )

    reachability = set()
    for variable in decomposed_matrices:
        for i in range(len(graph.nodes)):
            for j in range(len(graph.nodes)):
                if decomposed_matrices[variable][i, j] != 0:
                    reachability.add((variable, i, j))

    return reachability
