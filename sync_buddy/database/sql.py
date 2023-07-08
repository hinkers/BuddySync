from sqlalchemy import create_engine
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry

from sync_buddy.database.sql_table import define_table


@dataclass
class SqlRelationship:

    name: str
    key: str
    foreign: str
    foreign_table: str
    foreign_key: str


class SQL:

    connection_string: str
    _create_tables: bool
    tables: dict
    relationships = dict()
    mapper_registry = None
    echo: bool
    _engine = None
    _session = None

    def __init__(self, connection_string, create_tables=True, echo=False, *args, **kwargs):
        self.connection_string = connection_string
        self._create_tables = create_tables
        self.relationships = dict(one_to_many=[], one_to_one=[])
        self.mapper_registry = registry()
        self.echo = echo
        self.tables = dict()

    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.connection_string, echo=self.echo)
            self._session = sessionmaker(bind=self.engine())
        print(self._engine.url)
        return self._engine

    def session(self):
        if self._session is None:
            self._session = sessionmaker(bind=self.engine())
        return self._session

    def add_table(self, name, primary_key, columns):
        self.tables[name] = define_table(self, name, primary_key, columns)

    def add_relationships(self, type_, relationships):
        for definition in relationships:
            left, right = definition.split('->')
            table, key = left.split('.')
            foreign_table, foreign_key = right.split('.')
            self.relationships[type_].append(SqlRelationship(
                name=table,
                key=key.strip(),
                foreign=right.strip(),
                foreign_table=foreign_table.strip(),
                foreign_key=foreign_key.strip()
            ))

    def get_relationship(self, type_, table_name, column_name):
        for relationship in self.relationships[type_]:
            if relationship.name.lower() == table_name.lower() and relationship.key == column_name:
                return relationship
        return None

    def create_tables(self):
        if self._create_tables:
            self.mapper_registry.metadata.create_all(self.engine())
