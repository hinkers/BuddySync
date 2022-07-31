from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table)
from sqlalchemy.orm import relationship

valid_types = dict(
    Integer=Integer,
    String=String,
    DateTime=DateTime,
    Boolean=Boolean
)


class SqlTable:

    __key__: str
    __name__: str
    __columns__: list


def define_table(sql, name, key, column_definitions):
    columns = []
    column_names = []
    dependencies = []
    properties = dict()
    sql_relationships = sql.get_relationships(name)

    for c_name, c_type in column_definitions.items():
        nullable = False
        if c_type.endswith('?'):
            c_type = c_type[:-1]
            nullable = True
        assert c_type in valid_types, f'Invalid column type for "{c_name}"'
        column_names.append(c_name)
        if c_name in sql_relationships['one_to_many']:
            columns.append(Column(
                c_name,
                valid_types[c_type],
                ForeignKey(sql_relationships['one_to_many'][c_name].foreign),
                nullable=nullable
            ))
        elif c_name in sql_relationships['one_to_one']:
            columns.append(Column(
                c_name,
                valid_types[c_type],
                ForeignKey(sql_relationships['one_to_one'][c_name].foreign),
                nullable=nullable
            ))
        else:
            columns.append(Column(
                c_name,
                valid_types[c_type],
                primary_key=c_name == key,
                nullable=nullable
            ))

    for relation in sql.relationships['one_to_many']:
        if relation.foreign_table.lower() == name.lower():
            properties[relation.name.lower()] = relationship(
                relation.name,
                backref=relation.foreign_table.lower()
            )

    for relation in sql.relationships['one_to_one']:
        if relation.foreign_table.lower() == name.lower():
            properties[relation.name.lower()] = relationship(
                relation.name,
                backref=relation.foreign_table.lower(),
                uselist=False, 
            )

    table = Table(name, sql.mapper_registry.metadata, *columns)
    cls = type(name, (SqlTable, ), {
        '__key__': key,
        '__name__': name,
        '__columns__': column_names
    })

    sql.mapper_registry.map_imperatively(cls, table, properties=properties)
    return cls
