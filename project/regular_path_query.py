import cfpq_data
import networkx
import pyformlang
import scipy
from project.graph_utils import *
from project.automata_utils import *


def rpq_tensor(regex, graph, start_nodes=None, final_nodes=None):
    result = set()
    dfa = create_dfa_by_regex(regex)
    nfa = create_nfa_by_graph(graph, start_nodes, final_nodes)

    intersected_fa = intersect_two_fa(dfa, nfa)
    states = get_states_intersected(dfa, nfa)
    start_final_states = get_start_final_states_intersected(dfa, nfa)
    transitive_closure = get_transitive_closure(intersected_fa)

    for pair in transitive_closure:
        start = states[pair[0]]
        final = states[pair[1]]
        if (
            start in start_final_states["start"]
            and final in start_final_states["final"]
        ):
            result_pair = start[1], final[1]
            result.add(result_pair)

    return result
