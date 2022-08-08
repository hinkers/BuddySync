from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Integer, Interval, LargeBinary, Numeric,
                        SmallInteger, String, Table, Text, Time, Unicode,
                        UnicodeText)
from sqlalchemy.orm import relationship

valid_types = dict(
    BigInteger=BigInteger,
    Boolean=Boolean,
    Column=Column,
    Date=Date,
    DateTime=DateTime,
    Float=Float,
    ForeignKey=ForeignKey,
    Integer=Integer,
    Interval=Interval,
    LargeBinary=LargeBinary,
    Numeric=Numeric,
    SmallInteger=SmallInteger,
    String=String,
    Table=Table,
    Text=Text,
    Time=Time,
    Unicode=Unicode,
    UnicodeText=UnicodeText
)


class SqlTable:

    __key__: str
    __name__: str
    __columns__: list


def define_table(sql, name, key, column_definitions):
    columns = []
    column_names = []
    properties = dict()
    sql_relationships = sql.get_relationships(name)

    for c_name, c_type in column_definitions.items():
        args = [
            c_name,
            valid_types.get(c_type, None),
        ]
        kwargs = dict(
            primary_key=c_name == key,
            nullable=False
        )
        if c_type.endswith('?'):
            c_type = c_type[:-1]
            kwargs['nullable'] = True
            args[1] = valid_types.get(c_type, None)
        if c_type.endswith(')') and '(' in c_type:
            size = int(c_type[c_type.rfind('(') + 1:-1])
            c_type = c_type[:c_type.rfind('(')]
            args[1] = valid_types.get(c_type, None)(size)
        assert c_type in valid_types, f'Invalid column type for "{c_name}"'
        column_names.append(c_name)
        if c_name in sql_relationships['one_to_many']:
            args.append(ForeignKey(sql_relationships['one_to_many'][c_name].foreign))
        elif c_name in sql_relationships['one_to_one']:
            args.append(ForeignKey(sql_relationships['one_to_one'][c_name].foreign))
        columns.append(Column(*args, **kwargs))

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
