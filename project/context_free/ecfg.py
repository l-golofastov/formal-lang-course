from typing import Dict, Set
from pyformlang.cfg import Variable
from pyformlang.regular_expression import Regex


class ECFG:
    def __init__(
        self,
        variables: Set[Variable] = None,
        start_symbol: Variable = None,
        productions: Dict[Variable, Regex] = None,
    ):
        if variables is not None:
            variables = {self._to_variable(x) for x in variables}
        self.variables = variables or set()
        if start_symbol is not None:
            start_symbol = self._to_variable(start_symbol)
        self.start_symbol = start_symbol
        self.productions = productions or {}

    @staticmethod
    def _to_variable(given):
        if isinstance(given, Variable):
            return given
        return Variable(given)

    @staticmethod
    def ecfg_from_cfg(cfg):
        start_symbol = cfg.start_symbol or Variable("S")
        variables = set(cfg.variables or [])
        productions = {}

        for production in cfg.productions:
            head, body = production.head, production.body
            prev_body = productions.get(head)
            curr_body = Regex(".".join([symbol.value for symbol in body]) or "$")
            productions[head] = prev_body.union(curr_body) if prev_body else curr_body

        return ECFG(variables, start_symbol, productions)

    @staticmethod
    def ecfg_from_text(text, start_symbol=Variable("S")):
        variables = set()
        productions = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue

            head_text, body_text = line.split("->")
            head = Variable(head_text.strip())
            variables.add(head)
            body = Regex(body_text.strip())
            productions[head] = body

        return ECFG(variables, start_symbol, productions)

    @staticmethod
    def ecfg_from_file(file):
        with open(file) as f:
            ecfg = ECFG.ecfg_from_text(f.read())
        return ecfg
