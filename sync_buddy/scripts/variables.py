import pickle

from sync_buddy.scripts.variable import Variable


class Variables:

    __variable_names: list
    __variable_dict: dict

    def __init__(self):
        self.__variable_names = list()
        self.__variable_dict = dict()

    def load_variables(self, **kwargs):
        for key, value in kwargs.items():
            if key in ['__variable_names', '__variable_dict', 'as_dict', 'keys', 'format_string']:
                raise KeyError(f'Cannot name variable "{key}" as it is a reserved keyword.')
            self.__variable_dict[key] = value
            if (s_key := '{' + key + '}') not in self.__variable_names:
                self.__variable_names.append(s_key)
            setattr(self, key, value)

    def as_dict(self):
        return self.__variable_dict
    
    def keys(self):
        return self.__variable_names


def contains_variable(variables, input_string):
    return any(var_name in input_string for var_name in variables.keys())

def format_string(variables, replace_string):
    return replace_string.format(**variables.as_dict())

def initialize_variable(variables, var):
    if isinstance(var, str):
        return initialize_str_variable(variables, var)
    elif isinstance(var, (list, tuple)):
        return initialize_list_variable(variables, var)
    elif isinstance(var, dict):
        return initialize_dict_variable(variables, var)
    return var

def initialize_str_variable(variables, var):
    if contains_variable(variables, var):
        return Variable(var, variables)
    return var

def initialize_list_variable(variables, var_list):
    new_list = list()
    for var in var_list:
        new_list.append(initialize_variable(variables, var))
    return new_list

def initialize_dict_variable(variables, var_dict):
    for key in var_dict:
        var_dict[key] = initialize_variable(variables, var_dict[key])
    return var_dict

def save_variables(variables):
    with open('variables.p', 'wb') as pickle_file:
        pickle.dump(variables.as_dict(), pickle_file)

def load_variables(variables):
    try:
        with open('variables.p', 'rb') as pickle_file:
            return variables.load_variables(**pickle.load(pickle_file))
    except FileNotFoundError:
        return variables
