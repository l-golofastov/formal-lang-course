import cfpq_data
import networkx
import pydot
import pyformlang
import scipy


def get_nodes_edges_labels(name):
    nodes = name.number_of_nodes()
    edges = name.number_of_edges()
    labels = set(cfpq_data.get_sorted_labels(name))

    return nodes, edges, labels


def save_two_cycles_graph(nodes_graph1, nodes_graph2, labels, file_path):
    graph = cfpq_data.labeled_two_cycles_graph(
        nodes_graph1, nodes_graph2, labels=labels
    )

    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)

    return pydot_graph.write(path=file_path)


def create_dfa_by_regex(expression):
    regex = pyformlang.regular_expression.Regex(expression)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    minimal_dfa = dfa.minimize()

    return minimal_dfa


def create_nfa_by_graph(graph, start_nodes=None, final_nodes=None):
    nfa = pyformlang.finite_automaton.NondeterministicFiniteAutomaton()

    start_states = start_nodes if start_nodes is not None else list(graph.nodes)
    final_states = final_nodes if final_nodes is not None else list(graph.nodes)

    for state in start_states:
        nfa.add_start_state(state)

    for state in final_states:
        nfa.add_final_state(state)

    for node1, node2, label in list(graph.edges(data=True)):
        state1 = pyformlang.finite_automaton.State(node1)
        state2 = pyformlang.finite_automaton.State(node2)
        transition_symbol = pyformlang.finite_automaton.Symbol(label["label"])
        nfa.add_transition(state1, transition_symbol, state2)

    return nfa


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
    transitive_closure = sum(binary_matrices.values())
    prev = transitive_closure.count_nonzero()
    curr = 0

    while curr != prev:
        transitive_closure += transitive_closure @ transitive_closure
        prev = curr
        curr = transitive_closure.count_nonzero()

    return zip(*transitive_closure.nonzero())


def get_start_final_states_intersected(fa1, fa2):
    states = get_states_intersected(fa1, fa2)
    start_final_states_intersected = {}
    start_states_intersected = []
    final_states_intersected = []

    for start_state_fa1 in fa1.start_states:
        for start_state_fa2 in fa2.start_states:
            pair = start_state_fa1, start_state_fa2
            start_states_intersected.append(states[pair])

    for final_state_fa1 in fa1.final_states:
        for final_state_fa2 in fa2.final_states:
            pair = final_state_fa1, final_state_fa2
            final_states_intersected.append(states[pair])

    start_final_states_intersected["start"] = start_states_intersected
    start_final_states_intersected["final"] = final_states_intersected

    return start_final_states_intersected


def get_states_intersected(fa1, fa2):
    states = {}

    index = 0
    for state_fa1 in fa1.states:
        for state_fa2 in fa2.states:
            pair = state_fa1, state_fa2
            states[pair] = index
            index += 1

    return states


def make_regular_path_query(regex, graph, start_nodes=None, final_nodes=None):
    result = set()
    dfa = create_dfa_by_regex(regex)
    nfa = create_nfa_by_graph(graph, start_nodes, final_nodes)

    intersected_fa = intersect_two_fa(dfa, nfa)
    start_final_states = get_start_final_states_intersected(dfa, nfa)
    transitive_closure = get_transitive_closure(intersected_fa)

    for pair in transitive_closure:
        start = pair[0]
        final = pair[1]
        if start in start_final_states['start'] and final in start_final_states['final']:
            '''
            result_start = pair[0] // len(nfa.states)
            result_final = pair[1] // len(nfa.states)
            result.add((result_start, result_final))
            '''
            result.add(pair)
    return result
