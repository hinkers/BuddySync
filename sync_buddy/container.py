import re

from sync_buddy.database.sql import SQL
from sync_buddy.scripts.variables import Variables, load_variables, save_variables
from sync_buddy.utilities.utilites import Utilities


class GenericObject:

    def __init__(self, _dict):
        for name, value in _dict.items():
            setattr(self, camel_to_snake(name), value)


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


class Container:

    sql: SQL
    variables: Variables
    auth = object()
    endpoints = dict()
    sql = object()
    tables = dict()
    scripts = dict()
    run = dict()
    paginations = dict()

    def __init__(self):
        self.variables = Variables()
        self.utilities = Utilities(self)

    def load_variables(self):
        load_variables(self.variables)

    def save_variables(self):
        save_variables(self.variables)

    def endpoints_as_object(self):
        return GenericObject(self.endpoints)

    def pagination_as_object(self):
        return GenericObject({n: p.pages for n, p in self.paginations.items()})


container = Container()
