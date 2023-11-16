import scipy


def intersect_two_fa(fa1, fa2):
    binary_matrices_fa_intersected = {}

    binary_matrices_fa1 = create_binary_sparse_matrices(fa1)
    binary_matrices_fa2 = create_binary_sparse_matrices(fa2)

    for label in binary_matrices_fa1.keys() & binary_matrices_fa2.keys():
        binary_matrix_intersected = scipy.sparse.kron(
            binary_matrices_fa1[label], binary_matrices_fa2[label]
        )
        binary_matrices_fa_intersected[label] = binary_matrix_intersected

    return binary_matrices_fa_intersected


def create_binary_sparse_matrices(fa):
    matrices = {}
    fa_dict = fa.to_dict()

    number_of_states = len(fa.states)
    numerated_states = {state: index for index, state in enumerate(fa.states)}

    labels = set()
    for _, label, _ in fa:
        labels.add(label)
    labels_list = list(labels)

    for label in labels_list:
        matrix = scipy.sparse.dok_matrix(
            (number_of_states, number_of_states), dtype=int
        )
        for state in fa.states:
            if state in fa_dict and label in fa_dict[state]:
                transitions = fa_dict[state][label]
                transitions = (
                    transitions if isinstance(transitions, set) else {transitions}
                )
                for final_node in transitions:
                    matrix[numerated_states[state], numerated_states[final_node]] = 1
        matrices[label] = matrix
    return matrices


def get_transitive_closure(binary_matrices):
    if len(binary_matrices) == 0:
        return scipy.sparse.dok_matrix((0, 0), dtype=int)

    transitive_closure = sum(binary_matrices.values())
    prev = transitive_closure.count_nonzero()
    curr = 0

    while curr != prev:
        transitive_closure += transitive_closure @ transitive_closure
        prev = curr
        curr = transitive_closure.count_nonzero()

    return zip(*transitive_closure.nonzero())


def get_start_final_states_intersected(fa1, fa2):
    start_final_states_intersected = {}
    start_states_intersected = []
    final_states_intersected = []

    for start_state_fa1 in fa1.start_states:
        for start_state_fa2 in fa2.start_states:
            pair = start_state_fa1, start_state_fa2
            start_states_intersected.append(pair)

    for final_state_fa1 in fa1.final_states:
        for final_state_fa2 in fa2.final_states:
            pair = final_state_fa1, final_state_fa2
            final_states_intersected.append(pair)

    start_final_states_intersected["start"] = start_states_intersected
    start_final_states_intersected["final"] = final_states_intersected

    return start_final_states_intersected


def get_states_intersected(fa1, fa2):
    states = {}
    index = 0

    for state_fa1 in fa1.states:
        for state_fa2 in fa2.states:
            pair = state_fa1, state_fa2
            states[index] = pair
            index += 1

    return states


def create_direct_sum_binary_matrices(fa1, fa2):
    direct_sum_binary_matrices = {}

    fa1_decomposed = create_binary_sparse_matrices(fa1)
    fa2_decomposed = create_binary_sparse_matrices(fa2)

    labels = set()
    for _, label, _ in fa1:
        labels.add(label)
    for _, label, _ in fa2:
        labels.add(label)
    labels_list = list(labels)

    for label_dfa in fa1_decomposed:
        for label_nfa in fa2_decomposed:
            if label_dfa == label_nfa:
                fa1_label_matrix = fa1_decomposed[label_dfa]
                fa2_label_matrix = fa2_decomposed[label_nfa]

                matrix = scipy.sparse.dok_matrix(
                    (
                        len(fa1.states) + len(fa2.states),
                        len(fa1.states) + len(fa2.states),
                    ),
                    dtype=int,
                )

                for i in range(len(fa1.states)):
                    for j in range(len(fa1.states)):
                        matrix[i, j] = fa1_label_matrix.toarray()[i][j]

                for i in range((len(fa2.states))):
                    for j in range(len(fa2.states)):
                        matrix[
                            i + len(fa1.states), j + len(fa1.states)
                        ] = fa2_label_matrix.toarray()[i][j]

                direct_sum_binary_matrices[label_dfa] = matrix

                labels_list.remove(label_dfa)

    if len(labels_list) != 0:
        for label in labels_list:
            matrix = scipy.sparse.dok_matrix(
                (len(fa1.states) + len(fa2.states), len(fa1.states) + len(fa2.states)),
                dtype=int,
            )
            if label in fa1_decomposed:
                fa1_label_matrix = fa1_decomposed[label]
                for i in range(len(fa1.states)):
                    for j in range(len(fa1.states)):
                        matrix[i, j] = fa1_label_matrix.toarray()[i][j]
            else:
                fa2_label_matrix = fa2_decomposed[label]
                for i in range((len(fa2.states))):
                    for j in range(len(fa2.states)):
                        matrix[
                            i + len(fa1.states), j + len(fa1.states)
                        ] = fa2_label_matrix.toarray()[i][j]

            direct_sum_binary_matrices[label] = matrix

    return direct_sum_binary_matrices
