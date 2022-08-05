from sqlalchemy import create_engine
from dataclasses import dataclass
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import registry, relationship


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
    relationships = dict()
    mapper_registry = None
    echo: bool
    _engine = None
    _session = None

    def __init__(self, ConnectionString, CreateTables=True, Echo=False):
        self.connection_string = ConnectionString
        self._create_tables = True if CreateTables == 'True' else False
        self.relationships = dict(one_to_many=[], one_to_one=[])
        self.mapper_registry = registry()
        self.echo = True if Echo == 'True' else False

    def engine(self):
        if self._engine is None:
            self._engine = create_engine(self.connection_string, echo=self.echo)
            self._session = sessionmaker(bind=self.engine())
        return self._engine

    def session(self):
        if self._session is None:
            self._session = sessionmaker(bind=self.engine())
        return self._session

    def add_relationships(self, type_, relationships):
        for name, relation in relationships.items():
            key, foreign = relation.split('->')
            foreign_table, foreign_key = foreign.split('.')
            self.relationships[type_].append(SqlRelationship(
                name=name,
                key=key.strip(),
                foreign=foreign.strip(),
                foreign_table=foreign_table.strip(),
                foreign_key=foreign_key.strip()
            ))

    def get_relationships(self, name):
        return dict(
            one_to_many={ r.key: r for r in self.relationships['one_to_many'] if r.name.lower() == name.lower() },
            one_to_one={ r.key: r for r in self.relationships['one_to_one'] if r.name.lower() == name.lower() },
        )

    def create_tables(self):
        if self._create_tables:
            self.mapper_registry.metadata.create_all(self.engine())