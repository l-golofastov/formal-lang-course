import cfpq_data
import networkx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol


def get_graph(name):
    path = cfpq_data.download(name)

    return cfpq_data.graph_from_csv(path)


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
    regex = expression if isinstance(expression, Regex) else Regex(expression)
    enfa = regex.to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    minimal_dfa = dfa.minimize()

    return minimal_dfa


def create_nfa_by_graph(graph, start_nodes=None, final_nodes=None):
    nfa = NondeterministicFiniteAutomaton()

    start_states = start_nodes if start_nodes is not None else list(graph.nodes)
    final_states = final_nodes if final_nodes is not None else list(graph.nodes)

    for state in start_states:
        nfa.add_start_state(state)

    for state in final_states:
        nfa.add_final_state(state)

    for node1, node2, label in list(graph.edges(data=True)):
        state1 = State(node1)
        state2 = State(node2)
        transition_symbol = Symbol(label["label"])
        nfa.add_transition(state1, transition_symbol, state2)

    return nfa
