from typing import Dict
from pyformlang.cfg import Variable
from pyformlang.finite_automaton import EpsilonNFA


class RSM:
    def __init__(
        self, start_symbol: Variable = None, boxes: Dict[Variable, EpsilonNFA] = None
    ):
        self.start_symbol = start_symbol
        self.boxes = boxes

    @staticmethod
    def rsm_from_ecfg(ecfg):
        start_symbol = ecfg.start_symbol
        boxes = {
            variable: regex.to_epsilon_nfa()
            for variable, regex in ecfg.productions.items()
        }

        return RSM(start_symbol, boxes)

    def minimize(self):
        self.boxes = {
            variable: enfa.minimize() for variable, enfa in self.boxes.items()
        }

        return self
