from sql import SQL


class Container:

    sql: SQL
    auth = object()
    endpoints = dict()
    sql = object()
    tables = dict()
    scripts = dict()


container = Container()
