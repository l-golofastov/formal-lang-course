import numpy as np
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


def rpq_bfs(regex, graph, start_nodes=None, final_nodes=None, option=False):
    result = {} if option else set()
    dfa = create_dfa_by_regex(regex)
    nfa = create_nfa_by_graph(graph, start_nodes, final_nodes)

    dfa_states_indexes = {state: index for index, state in enumerate(dfa.states)}
    dfa_indexes_states = {index: state for state, index in dfa_states_indexes.items()}
    nfa_states_indexes = {
        state: (index + len(dfa_states_indexes))
        for index, state in enumerate(nfa.states)
    }
    nfa_indexes_states = {index: state for state, index in nfa_states_indexes.items()}

    direct_sum_decomposed = create_direct_sum_binary_matrices(dfa, nfa)

    mask = scipy.sparse.dok_matrix((1, len(dfa.states) + len(nfa.states)), dtype=int)
    for j in range(len(dfa.states) + len(nfa.states)):
        mask[0, j] = 1

    for start_state_dfa in dfa.start_states:
        for start_state_nfa in nfa.start_states:
            if option:
                reachable_states = set()
            start_state_dfa_num = dfa_states_indexes[start_state_dfa]
            start_state_nfa_num = nfa_states_indexes[start_state_nfa]

            front_prev = scipy.sparse.dok_matrix(
                (1, len(dfa.states) + len(nfa.states)), dtype=int
            )
            front = scipy.sparse.dok_matrix(
                (1, len(dfa.states) + len(nfa.states)), dtype=int
            )
            front[0, start_state_dfa_num] = 1
            front[0, start_state_nfa_num] = 1

            while not (np.array_equal(front_prev.toarray(), front.toarray())):
                for j in range(len(dfa.states) + len(nfa.states)):
                    front_element_reversed = 1 if front[0, j] == 0 else 0
                    mask[0, j] = 1 if (mask[0, j] * front_element_reversed > 0) else 0

                multiplication_result = {}
                for label in direct_sum_decomposed:
                    multiplication_result[label] = front @ direct_sum_decomposed[label]

                front_prev = front
                front = sum(multiplication_result.values())
                for j in range(len(dfa.states) + len(nfa.states)):
                    front[0, j] = 1 if (front[0, j] * mask[0, j] > 0) else 0

                for j in range(len(dfa.states), front.shape[1]):
                    if front[0, j] == 1:
                        if nfa_indexes_states[j] in nfa.final_states:
                            if option:
                                reachable_states.add(j - len(dfa.states))
                            else:
                                result.add(j - len(dfa.states))

            if option:
                result[start_state_nfa_num] = reachable_states

    return result
