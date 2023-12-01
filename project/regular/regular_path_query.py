from project.regular.graph_utils import *
from project.regular.automata_utils import *


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
    dfa = create_dfa_by_regex(regex)
    nfa = create_nfa_by_graph(graph, start_nodes, final_nodes)

    common_labels = set()
    for _, label_dfa, _ in dfa:
        for _, label_nfa, _ in nfa:
            if label_dfa == label_nfa:
                common_labels.add(label_dfa)

    result = bfs_two_graph(dfa, nfa, common_labels, option)

    return result


def bfs_two_graph(dfa, nfa, common_labels, option=False):
    result = {} if option else set()
    if len(dfa.states) == 0 or len(nfa.states) == 0:
        return result

    dfa_states_indexes = {state: index for index, state in enumerate(dfa.states)}
    dfa_indexes_states = {index: state for state, index in dfa_states_indexes.items()}
    nfa_states_indexes = {
        state: (index + len(dfa_states_indexes))
        for index, state in enumerate(nfa.states)
    }
    nfa_indexes_states = {index: state for state, index in nfa_states_indexes.items()}

    direct_sum_decomposed = create_direct_sum_binary_matrices(dfa, nfa)

    for start_state_dfa in dfa.start_states:
        for start_state_nfa in nfa.start_states:
            reachable_states = set()
            start_state_dfa_num = dfa_states_indexes[start_state_dfa]
            start_state_nfa_num = nfa_states_indexes[start_state_nfa]

            mask = scipy.sparse.dok_matrix(
                (1, len(dfa.states) + len(nfa.states)), dtype=int
            )
            for j in range(len(dfa.states) + len(nfa.states)):
                mask[0, j] = 1

            front = scipy.sparse.dok_matrix(
                (1, len(dfa.states) + len(nfa.states)), dtype=int
            )
            front[0, start_state_dfa_num], front[0, start_state_nfa_num] = 1, 1

            prev = 0
            curr = mask.count_nonzero()

            while prev != curr:
                for j in range(len(dfa.states) + len(nfa.states)):
                    front_element_reversed = 1 if front[0, j] == 0 else 0
                    mask[0, j] = 1 if (mask[0, j] * front_element_reversed > 0) else 0

                front_dfa_prev = [
                    (1 if front[0, j] != 0 else 0) for j in range(len(dfa.states))
                ]
                transition_labels_dfa = set()

                multiplication_result = {}
                for label in direct_sum_decomposed:
                    multiplication_result[label] = front @ direct_sum_decomposed[label]

                multiplication_sum_premature = sum(multiplication_result.values())
                front_empty = scipy.sparse.dok_matrix(
                    (1, len(dfa.states) + len(nfa.states)), dtype=int
                )
                front_premature = (
                    front_empty
                    if type(multiplication_sum_premature) == int
                    else multiplication_sum_premature
                )
                front_dfa_curr = [
                    (1 if front_premature[0, j] != 0 else 0)
                    for j in range(len(dfa.states))
                ]

                for prev_dfa_state in range(len(front_dfa_prev)):
                    for curr_dfa_state in range(len(front_dfa_curr)):
                        if (
                            front_dfa_prev[prev_dfa_state] == 1
                            and front_dfa_curr[curr_dfa_state] == 1
                        ):
                            for state1, label, state2 in dfa:
                                if (
                                    state1 == dfa_indexes_states[prev_dfa_state]
                                    and state2 == dfa_indexes_states[curr_dfa_state]
                                    and label in common_labels
                                ):
                                    transition_labels_dfa.add(label)

                multiplication_sum = scipy.sparse.dok_matrix(
                    (1, len(dfa.states) + len(nfa.states)), dtype=int
                )
                for label in transition_labels_dfa:
                    multiplication_sum += multiplication_result[label]

                front = (
                    front_empty
                    if type(multiplication_sum) == int
                    else multiplication_sum
                )

                for dfa_state in range(len(dfa.states)):
                    for nfa_state in range(
                        len(dfa.states), len(dfa.states) + len(nfa.states)
                    ):
                        if front[0, dfa_state] != 0 and front[0, nfa_state] != 0:
                            if (
                                dfa_indexes_states[dfa_state] in dfa.final_states
                                and nfa_indexes_states[nfa_state] in nfa.final_states
                            ):
                                if option:
                                    reachable_states.add(nfa_state - len(dfa.states))
                                else:
                                    result.add(nfa_state - len(dfa.states))

                prev = curr
                curr = mask.count_nonzero()

            if option:
                result[start_state_nfa_num - len(dfa.states)] = reachable_states

    return result
