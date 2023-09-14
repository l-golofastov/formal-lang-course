import cfpq_data
import networkx
import pydot


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
