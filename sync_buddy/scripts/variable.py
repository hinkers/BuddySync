from string import Template


class Variable:

    replace_string: str
    variables: object

    def __init__(self, replace_string, variables):
        self.replace_string = replace_string
        self.variables = variables

    def __repr__(self):
        return self.format_string()

    def __str__(self):
        return str(self.__repr__())

    def format_string(self):
        return Template(self.replace_string).safe_substitute(self.variables.as_dict())
