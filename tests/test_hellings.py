from cfpq_data import labeled_two_cycles_graph
from pyformlang.cfg.cfg import CFG
from project.context_free.cfg import *
from project.context_free.hellings import *


def test_hellings():
    graph = labeled_two_cycles_graph(2, 2, labels=("a", "b"))

    print()
    print(graph.edges(data="label"))

    cfg = CFG.from_text(
        """
        S -> a | $
    """
    )

    transitions = hellings(cfg, graph)
    print(transitions)

    assert True
