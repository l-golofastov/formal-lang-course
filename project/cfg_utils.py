from pyformlang.cfg import CFG


def get_weak_chomsky_normal_form(grammar):
    new_grammar = grammar.eliminate_unit_productions().remove_useless_symbols()
    new_productions = new_grammar._get_productions_with_only_single_terminals()
    new_productions = new_grammar._decompose_productions(new_productions)

    return CFG(start_symbol=new_grammar.start_symbol, productions=set(new_productions))


def read_cfg_from_file(path):
    with open(path, "r") as file:
        grammar = file.read()

    return CFG.from_text(grammar)
