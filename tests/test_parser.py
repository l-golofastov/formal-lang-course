import filecmp
import os
from project.gql.parser import *


def test_accapts_print():
    inp_true = "print (expr);"
    inp_false = "print .not_expr;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False


def test_accapts_var():
    inp_true = "good_variable = true;"
    inp_false = "1_bad_variable = false;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False


def test_accepts_val():
    inp_true = "good_value = 42;"
    inp_false = "bad_value = 0123456789;"

    assert accepts(inp_true) == True
    assert accepts(inp_false) == False
