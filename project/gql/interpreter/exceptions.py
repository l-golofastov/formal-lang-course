class SomethingException(Exception):
    """
    Exception in interpretation.
    """

    def __init__(self, msg: str):
        self.msg = msg


class IncorrectExtensionException(SomethingException):
    def __init__(self):
        self.msg = "The file must have the extension *qgl"


class IncorrectPathException(SomethingException):
    def __init__(self, filename: str):
        self.msg = "Couldn't open the file" + filename


class IncorrectSyntaxError(SomethingException):
    def __init__(self):
        self.msg = "The syntax of the program does not match the parser"


class UnknownVariableException(SomethingException):
    def __init__(self, name: str):
        self.msg = "Couldn't find the variable" + name


class RemoveGlobalScopeException(SomethingException):
    def __init__(self):
        self.msg = "The global scope cannot be removed"


class LoadGraphException(SomethingException):
    def __init__(self, name: str):
        self.msg = "Couldn't load the graph " + name


class TypeException(SomethingException):
    def __init__(self, expected: str, actual: str):
        self.msg = "Expected the variable of type: " + expected + ", but got: " + actual
