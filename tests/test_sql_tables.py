import pytest
from sqlalchemy import Integer, String, inspect
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry, sessionmaker

from sync_buddy.database.sql import SQL, SqlRelationship
from sync_buddy.database.sql_table import SqlTable


@pytest.fixture
def connection_string():
    return 'sqlite://'  # Memory only database


class TestSQL:
    @staticmethod
    def create_sql_instance(connection_string):
        return SQL(connection_string)

    def test_sql_init(self, connection_string):
        sql = self.create_sql_instance(connection_string)

        assert sql.connection_string == connection_string
        assert sql._create_tables == True
        assert sql.echo == False
        assert sql.tables == {}
        assert sql.relationships == {"one_to_many": [], "one_to_one": []}
        assert isinstance(sql.mapper_registry, registry)

    def test_sql_engine(self, connection_string):
        sql = self.create_sql_instance(connection_string)
        engine = sql.engine()

        assert isinstance(engine, Engine)
        assert str(engine.url) == connection_string
        assert engine.echo == False

    def test_sql_session(self, connection_string):
        sql = self.create_sql_instance(connection_string)
        session = sql.session()

        assert isinstance(session, sessionmaker)

    def test_sql_add_table(self, connection_string):
        sql = self.create_sql_instance(connection_string)

        name = "my_table"
        primary_key = "id"
        columns = dict(
            id='Integer',
            name='String',
            age='Integer'
        )
        sql.add_table(name, primary_key, columns)

        assert name in sql.tables
        assert issubclass(sql.tables[name], SqlTable)

    def test_sql_add_relationships(self, connection_string):
        sql = self.create_sql_instance(connection_string)

        relationships = ["table1.id -> table2.foreign_key", "table3.id -> table4.foreign_key"]
        sql.add_relationships("one_to_many", relationships)

        assert len(sql.relationships["one_to_many"]) == 2
        assert isinstance(sql.relationships["one_to_many"][0], SqlRelationship)
        assert sql.relationships["one_to_many"][0].name == "table1"
        assert sql.relationships["one_to_many"][0].key == "id"
        assert sql.relationships["one_to_many"][0].foreign == "table2.foreign_key"
        assert sql.relationships["one_to_many"][0].foreign_table == "table2"
        assert sql.relationships["one_to_many"][0].foreign_key == "foreign_key"

    def test_sql_get_relationships(self, connection_string):
        sql = self.create_sql_instance(connection_string)

        relationships = [
            SqlRelationship("table1", "id", "table2.foreign_key", "table2", "foreign_key"),
            SqlRelationship("table1", "id", "table3.foreign_key", "table3", "foreign_key"),
            SqlRelationship("table2", "id", "table4.foreign_key", "table4", "foreign_key"),
        ]
        sql.relationships = {
            "one_to_many": relationships,
            "one_to_one": [],
        }

        table1_relationships = sql.get_relationship("one_to_many", "table1", "id")
        assert isinstance(table1_relationships, SqlRelationship)
        assert table1_relationships.name == "table1"
        assert table1_relationships.key == "id"
        assert table1_relationships.foreign == "table2.foreign_key"
        assert table1_relationships.foreign_table == "table2"
        assert table1_relationships.foreign_key == "foreign_key"

        table2_relationships = sql.get_relationship("one_to_many", "table2", "id")
        assert isinstance(table2_relationships, SqlRelationship)
        assert table2_relationships.name == "table2"
        assert table2_relationships.key == "id"
        assert table2_relationships.foreign == "table4.foreign_key"
        assert table2_relationships.foreign_table == "table4"
        assert table2_relationships.foreign_key == "foreign_key"

        non_existing_relationship = sql.get_relationship("one_to_many", "table1", "non_existing_column")
        assert non_existing_relationship is None

    def test_sql_create_tables(self, connection_string):
        sql = self.create_sql_instance(connection_string)

        name = "my_table"
        primary_key = "id"
        columns = dict(
            id='Integer',
            name='String',
            age='Integer'
        )
        sql.add_table(name, primary_key, columns)

        sql.create_tables()
        
        assert inspect(sql.engine()).has_table("my_table")

        columns = inspect(sql.engine()).get_columns("my_table")
        assert any(c["name"] == 'id' for c in columns)
        assert any(c["name"] == 'name' for c in columns)
        assert any(c["name"] == 'age' for c in columns)
        assert all(c["name"] != 'tiger' for c in columns)
        assert any(c["name"] == 'id' and isinstance(c['type'], Integer) for c in columns)
        assert any(c["name"] == 'name' and isinstance(c['type'], String) for c in columns)
        assert any(c["name"] == 'age' and isinstance(c['type'], Integer) for c in columns)
