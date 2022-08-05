class Variables:

    __variable_names: list
    __variable_dict: dict

    def __init__(self):
        self.__variable_names = list()
        self.__variable_dict = dict()

    def load_variables(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['__variable_names', '__variable_dict', 'load_variables', 'contains_variable', 'format_string']:
                raise KeyError(f'Cannot name variable "{key}" as it is a reserved keyword.')
            self.__variable_names.append('{' + key + '}')
            self.__variable_dict[key] = value
            setattr(self, key, value)

    def contains_variable(self, input_string):
        return any(var_name in input_string for var_name in self.__variable_names)

    def format_string(self, replace_string):
        return replace_string.format(**self.__variable_dict)

