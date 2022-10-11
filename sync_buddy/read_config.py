from sys import getsizeof
from typing import List

import hiyapyco
from dotenv import dotenv_values

from container import Container
from sync_buddy.database.sql import SQL
from sync_buddy.database.sql_table import define_table
from sync_buddy.logger import get_logger
from sync_buddy.scripts.custom_script import CustomScript
from sync_buddy.web.api import Api
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.pagination.factory import create_pagination


def read_config(filenames: List[str]) -> Container:
    logger = get_logger('app')

    env = dotenv_values(".env")
    logger.debug(f'Read {len(env.keys())} values from .env file')

    container = Container()

    merged_config = hiyapyco.load(
        *filenames,
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
    )
    logger.debug(f'Read all yaml files {getsizeof(merged_config)} bytes')

    yaml_string = hiyapyco.dump(merged_config)
    for v_name, v_value in env.items():
        yaml_string = yaml_string.replace(f'${{{v_name}}}', v_value)
    config = hiyapyco.load(yaml_string, interpolate=True)
    logger.debug(f'Yaml files variable interpolation complete, new size {getsizeof(merged_config)} bytes')

    apis = {definition.get('name', 'default'): Api(**definition) for definition in config['api']}
    logger.debug(f'Loaded {len(apis)} API definitions')

    container.endpoints = {
        definition.get('name', 'default'): Endpoint(apis['default'], container, **definition)
        for definition in config['api'][0]['endpoint']
    }
    logger.debug(f'Loaded {len(container.endpoints)} Endpoint definitions')

    container.paginations = {
        definition.get('name', 'default'): create_pagination(**definition)
        for definition in config['pagination']
    }
    logger.debug(f'Loaded {len(container.paginations)} Pagination definitions')

    container.sql = {definition.get('name', 'default'): SQL(**definition) for definition in config['sql']}
    logger.debug(f'Loaded {len(container.sql)} SQL definitions')

    container.variables.load_variables(**config['variable'])
    container.scripts = [CustomScript(filepath, container) for filepath in config['run']]
    logger.debug(f'Loaded {len(container.scripts)} total scripts')

    container.load_variables()
    logger.debug(f'Config variables updated')

    container.sql['default'].add_relationships(
        'one_to_many',
        config['sql'][0]['relationship'].get('one_to_many', dict())
    )
    logger.debug(f'Loaded {len(container.sql["default"].relationships["one_to_many"])} one to many relationships')

    container.sql['default'].add_relationships(
        'one_to_one',
        config['sql'][0]['relationship'].get('one_to_one', dict())
    )
    logger.debug(f'Loaded {len(container.sql["default"].relationships["one_to_one"])} one to one relationships')

    container.tables = {
        definition.get('name', 'default'): define_table(container.sql['default'], definition.get('name', 'default'), definition['primary_key'], definition['columns'])
        for definition in config['sql'][0]['table']
    }
    logger.debug(f'Loaded {len(container.tables)} table definitions')

    logger.info('Finished reading config, valid')
    return container
