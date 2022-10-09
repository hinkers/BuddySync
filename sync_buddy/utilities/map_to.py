from typing import Any

from sync_buddy.database.sql_table import SqlTable


def map_to(self: object, filter_obj: Any, data: dict, mapping: dict = None, funcs: dict = None) -> dict:
    retval = dict()
    mapping = mapping or dict()
    funcs = funcs or dict()

    if issubclass(filter_obj, SqlTable):
        for column in filter_obj.__columns__:
            if column in mapping:
                retval[column] = data[mapping[column]]
            elif column in data:
                retval[column] = data[column]
        
        for column in retval:
            if column in funcs:
                if isinstance(funcs[column], (list, tuple)):
                    func = funcs[column][0]
                    args = funcs[column][1] if len(funcs[column]) >= 2 else list()
                    kwargs = funcs[column][2] if len(funcs[column]) >= 3 else dict()
                else:
                    func = funcs[column]
                    args = list()
                    kwargs = dict()
                retval[column] = func(*[retval[column], *args], **kwargs)

        for column, table_name in filter_obj.__relationships__.items():
            table = self._container.tables[table_name]
            if column in mapping:
                retval[column] = self.map_to(
                    table,
                    data[mapping[column]],
                    mapping[column],
                    funcs[column] if column in funcs else None
                )
            elif column in data:
                retval[column] = self.map_to(
                    table,
                    data[column],
                    funcs=funcs[column] if column in funcs else None
                )
        return filter_obj(**retval)

    raise ValueError(f'Unknown filter_obj type "{type(filter_obj).__name__}"')
