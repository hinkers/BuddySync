from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import mapper

metadata = MetaData()
valid_types = dict(
    Integer=Integer,
    String=String,
    DateTime=DateTime
)


class SqlTable:
    
    __key__: str
    __name__: str
    __table__: str
    __columns__: list

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


def define_table(engine, name, key, **column_definitions):
    columns = []
    column_names = []
    for c_name, c_type in column_definitions.items():
        assert c_type in valid_types, f'Invalid column type for "{c_name}"'
        column_names.append(c_name)
        columns.append(Column(c_name, valid_types[c_type], primary_key=c_name == key))
    table = Table(name, metadata, *columns)

    cls = type(name, (SqlTable, ), {
        '__key__': key,
        '__name__': name,
        '__columns__': column_names
    })

    mapper(cls, table)
    return cls
