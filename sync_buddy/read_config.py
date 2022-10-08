import configparser
from typing import List

from dotenv import dotenv_values

from container import Container, container
from sync_buddy.database.sql import SQL
from sync_buddy.database.sql_table import define_table
from sync_buddy.scripts.custom_script import CustomScript
from sync_buddy.web.api import Api
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.pagination.factory import create_pagination


def read_config(filenames: List[str]) -> Container:
    env = dotenv_values(".env")

    config = configparser.RawConfigParser()
    config.optionxform = str

    raw_tables = dict()
    one_to_many = dict()
    one_to_one = dict()

    for filename in filenames:
        with open(filename, 'r') as config_file:
            config_string = config_file.read()
            for v_name, v_value in env.items():
                config_string = config_string.replace(
                    f'${{{v_name}}}', v_value)
            config.read_string(config_string)

    for section in config.sections():
        if section == 'Authentication':
            api = Api(**config[section])
        elif section == 'SQL':
            container.sql = SQL(**config[section])
        elif section == 'Relationships:OneToMany':
            one_to_many = dict(**one_to_many, **config[section])
        elif section == 'Relationships:OneToOne':
            one_to_one = dict(**one_to_one, **config[section])
        elif section == 'Run':
            container.run = dict(**container.run, **config[section])
        elif section == 'Variables':
            container.variables.load_variables(**config[section])
        elif section == 'Scripts':
            container.scripts = dict(
                **container.scripts,
                **{
                    name: CustomScript(s_name, container)
                    for name, s_name in config[section].items()
                }
            )
        elif ':' in section:
            s_type, s_name = section.split(':', 1)
            if s_type == 'Table':
                raw_tables[s_name] = config[section]
            elif s_type == 'Endpoint':
                container.endpoints[s_name] = Endpoint(
                    s_name, container, **config[section])
            elif s_type == 'Pagination':
                container.paginations[s_name] = create_pagination(
                    **config[section])
            else:
                raise KeyError(f"Unknown section type '{section}'")
        else:
            raise KeyError(f"Unknown section type '{section}'")

    container.load_variables()

    container.sql.add_relationships('one_to_many', one_to_many)
    container.sql.add_relationships('one_to_one', one_to_one)

    for name, tbl in raw_tables.items():
        columns = dict(**tbl)
        del columns['__key__']
        container.tables[name] = define_table(
            container.sql, name, tbl['__key__'], columns)

    for endpoint in container.endpoints.values():
        endpoint.api = api

    return container
