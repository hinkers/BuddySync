from apisync.database.sql import SQL
from apisync.scripts.variables import Variables


class Container:

    sql: SQL
    variables: Variables
    auth = object()
    endpoints = dict()
    sql = object()
    tables = dict()
    scripts = dict()

    def __init__(self):
        self.variables = Variables()


container = Container()
