import re

from sync_buddy.database.sql import SQL
from sync_buddy.scripts.variables import Variables, load_variables, save_variables


class Endpoints:
    pass


class Pagination:
    pass


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

    def load_variables(self):
        self.variables = load_variables(self.variables)

    def save_variables(self):
        save_variables(self.variables)

    def endpoints_as_object(self):
        endpoints = Endpoints()

        for name, endpoint in self.endpoints.items():
            setattr(endpoints, camel_to_snake(name), endpoint)

        return endpoints

    def pagination_as_object(self):
        paginations = Pagination()

        for name, pagination in self.paginations.items():
            setattr(pagination, camel_to_snake(name), pagination)

        return paginations



container = Container()
