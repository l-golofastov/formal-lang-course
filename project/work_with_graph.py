import cfpq_data
import networkx
import pydot
import pyformlang


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


def get_dfa_by_regex(expression):
    regex = pyformlang.regular_expression.Regex(expression)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    minimal_dfa = dfa.minimize()

    return minimal_dfa


def get_nfa_by_graph(graph, start_nodes=[], final_nodes=[]):
    nfa = pyformlang.finite_automaton.NondeterministicFiniteAutomaton()

    if start_nodes:
        for node in start_nodes:
            nfa.add_start_state(node)
    else:
        for node in list(graph.nodes):
            nfa.add_start_state(node)

    if final_nodes:
        for node in final_nodes:
            nfa.add_final_state(node)
    else:
        for node in list(graph.nodes):
            nfa.add_final_state(node)

    for node1, node2, label in list(graph.edges(data=True)):
        state1 = pyformlang.finite_automaton.State(node1)
        state2 = pyformlang.finite_automaton.State(node2)
        transition_symbol = pyformlang.finite_automaton.Symbol(label["label"])
        nfa.add_transition(state1, transition_symbol, state2)

    return nfa
