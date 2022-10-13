from enum import Enum
import re

from schema import And, Optional, Or, Regex, Schema, Use


class Column(Enum):    
    BigInteger = 'BigInteger'
    Boolean = 'Boolean'
    Column = 'Column'
    Date = 'Date'
    DateTime = 'DateTime'
    Float = 'Float'
    ForeignKey = 'ForeignKey'
    Integer = 'Integer'
    Interval = 'Interval'
    LargeBinary = 'LargeBinary'
    Numeric = 'Numeric'
    SmallInteger = 'SmallInteger'
    String = 'String'
    Table = 'Table'
    Text = 'Text'
    Time = 'Time'
    Unicode = 'Unicode'
    UnicodeText = 'UnicodeText'


def validate_sql(data):
    VALID_RELATIONSHIP = And(str, Use(str.strip), Regex('.*\..*\s*->\s*.*\..*', flags=re.IGNORECASE))
    VALID_COLUMN = Regex('|'.join([f'{e.value}(?:\(.*\))?' for e in Column]), flags=re.IGNORECASE)

    return Schema({
        Optional('name'): And(str, len),
        'connection_string': And(str, len),
        'create_tables': Use(bool),
        'relationships': {
            Optional('one_to_one'): [VALID_RELATIONSHIP],
            Optional('one_to_many'): [VALID_RELATIONSHIP]
        },
        'tables': [{
            'name': str,
            'primary_key': str,
            'columns': {
                str: VALID_COLUMN
            }
        }]
    }).validate(data)


def validate_sqls(data):
    return Schema([Use(validate_sql)]).validate(data)
