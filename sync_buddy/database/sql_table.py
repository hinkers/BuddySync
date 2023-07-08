from sqlalchemy import (BigInteger, Boolean, Column, Date, DateTime, Float,
                        ForeignKey, Integer, Interval, LargeBinary, Numeric,
                        SmallInteger, String, Table, Text, Time, Unicode,
                        UnicodeText)
from sqlalchemy.orm import relationship

from sync_buddy.database.schema import Column as ColumnEnum
from sync_buddy.logger import get_logger

type_mapping = {
    ColumnEnum.BigInteger.value: BigInteger,
    ColumnEnum.Boolean.value: Boolean,
    ColumnEnum.Column.value: Column,
    ColumnEnum.Date.value: Date,
    ColumnEnum.DateTime.value: DateTime,
    ColumnEnum.Float.value: Float,
    ColumnEnum.ForeignKey.value: ForeignKey,
    ColumnEnum.Integer.value: Integer,
    ColumnEnum.Interval.value: Interval,
    ColumnEnum.LargeBinary.value: LargeBinary,
    ColumnEnum.Numeric.value: Numeric,
    ColumnEnum.SmallInteger.value: SmallInteger,
    ColumnEnum.String.value: String,
    ColumnEnum.Table.value: Table,
    ColumnEnum.Text.value: Text,
    ColumnEnum.Time.value: Time,
    ColumnEnum.Unicode.value: Unicode,
    ColumnEnum.UnicodeText.value: UnicodeText
}


class SqlTable:

    __key__: str
    __name__: str
    __columns__: list
    __relationships__: dict


def define_table(sql, name, key, column_definitions):
    logger = get_logger('database')

    columns = []
    column_names = []
    properties = dict()
    relationships = dict()

    for c_name, c_type in column_definitions.items():
        args = [
            c_name,
            type_mapping.get(c_type, None),
        ]
        kwargs = dict(
            primary_key=c_name == key,
            nullable=False
        )
        if c_type.endswith('?'):
            c_type = c_type[:-1]
            kwargs['nullable'] = True
            args[1] = type_mapping.get(c_type, None)
        if c_type.endswith(')') and '(' in c_type:
            size = int(c_type[c_type.rfind('(') + 1:-1])
            c_type = c_type[:c_type.rfind('(')]
            args[1] = type_mapping.get(c_type, None)(size)
        assert c_type in type_mapping, f'Invalid column type for "{c_name}"'
        column_names.append(c_name)
        
        one_to_many = sql.get_relationship('one_to_many', name, c_name)
        one_to_one = sql.get_relationship('one_to_one', name, c_name)
        if one_to_many is not None:
            args.append(ForeignKey(one_to_many.foreign))
        elif one_to_one is not None:
            args.append(ForeignKey(one_to_one.foreign))
        
        columns.append(Column(*args, **kwargs))

    for relation in sql.relationships['one_to_many']:
        if relation.foreign_table.lower() == name.lower():
            properties[relation.name.lower()] = relationship(
                relation.name,
                backref=relation.foreign_table.lower()
            )
            relationships[relation.name.lower()] = relation.name

    for relation in sql.relationships['one_to_one']:
        if relation.foreign_table.lower() == name.lower():
            properties[relation.name.lower()] = relationship(
                relation.name,
                backref=relation.foreign_table.lower(),
                uselist=False, 
            )
            relationships[relation.name.lower()] = relation.name

    table = Table(name, sql.mapper_registry.metadata, *columns)
    cls = type(name, (SqlTable, ), {
        '__key__': key,
        '__name__': name,
        '__columns__': column_names,
        '__relationships__': relationships
    })

    sql.mapper_registry.map_imperatively(cls, table, properties=properties)
    logger.debug(f'Created table class {name}')
    return cls
