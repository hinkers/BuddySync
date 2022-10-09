from typing import List

import hiyapyco
from dotenv import dotenv_values

from container import Container
from sync_buddy.database.sql import SQL
from sync_buddy.database.sql_table import define_table
from sync_buddy.scripts.custom_script import CustomScript
from sync_buddy.web.api import Api
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.pagination.factory import create_pagination


def read_config(filenames: List[str]) -> Container:
    env = dotenv_values(".env")

    container = Container()

    merged_config = hiyapyco.load(
        *filenames,
        method=hiyapyco.METHOD_MERGE,
        interpolate=True,
        castinterpolated=True,
        failonmissingfiles=True
    )

    yaml_string = hiyapyco.dump(merged_config)
    for v_name, v_value in env.items():
        yaml_string = yaml_string.replace(f'${{{v_name}}}', v_value)
    config = hiyapyco.load(yaml_string)

    apis = {name: Api(**definition) for name, definition in config['api'].items()}
    container.endpoints = {
        name: Endpoint(name, apis['default'], container, **definition)
        for name, definition in config['api']['default']['endpoint'].items()
    }
    container.paginations = {
        name: create_pagination(**definition)
        for name, definition in config['pagination'].items()
    }
    container.sql = {name: SQL(**definition) for name, definition in config['sql'].items()}
    container.run = config['run']
    container.variables.load_variables(**config['variable'])
    container.scripts = {
        name: CustomScript(s_name, container)
        for name, s_name in config['script'].items()
    }

    container.load_variables()

    container.sql['default'].add_relationships(
        'one_to_many',
        config['sql']['default']['relationship'].get('one_to_many', dict())
    )
    container.sql['default'].add_relationships(
        'one_to_one',
        config['sql']['default']['relationship'].get('one_to_one', dict())
    )

    container.tables = {
        name: define_table(container.sql['default'], name, table['primary_key'], table['columns'])
        for name, table in config['sql']['default']['table'].items()
    }

    return container
