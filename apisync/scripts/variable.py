from apisync.scripts.variables import Variables


class Variable:

    replace_string: str
    variables: Variables

    def __init__(self, replace_string, variables):
        self.replace_string = replace_string
        self.variables = variables

    def __repr__(self):
        return self.variables.format_string(self.replace_string)

    def __str__(self):
        return str(self.__repr__())
