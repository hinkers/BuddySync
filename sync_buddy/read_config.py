from sys import getsizeof
from typing import List

import hiyapyco
from dotenv import dotenv_values

from sync_buddy.container import Container
from sync_buddy.database.schema import validate_sqls
from sync_buddy.logger import get_logger
from sync_buddy.scripts.scheme import validate_scripts, validate_variables
from sync_buddy.web.schema import validate_apis, validate_paginations


def read_config(filenames: List[str]) -> Container:
    # Get logger
    logger = get_logger('app')

    # Get environment variables
    env = dotenv_values(".env")
    logger.debug(f'Read {len(env.keys())} values from .env file')

    # Read all config files and merge the results
    merged_config = hiyapyco.load(
        *filenames,
        method=hiyapyco.METHOD_MERGE,
        failonmissingfiles=True
    )
    logger.debug(f'Read all yaml files {getsizeof(merged_config)} bytes')

    # Replace values with environment variables
    yaml_string = hiyapyco.dump(merged_config)
    for v_name, v_value in env.items():
        yaml_string = yaml_string.replace(f'${{{v_name}}}', v_value)
    config = hiyapyco.load(yaml_string, interpolate=True)
    logger.debug(f'Yaml files variable interpolation complete, new size {getsizeof(merged_config)} bytes')

    # Validate schema
    apis = validate_apis(config.get('apis', []))
    paginations = validate_paginations(config.get('paginations', []))
    variables = validate_variables(config.get('variables', {}))
    scripts = validate_scripts(config.get('scripts', []))
    sqls = validate_sqls(config.get('sqls', []))
    logger.info('All config is valid')

    # Create container
    container = Container(apis, paginations, variables, scripts, sqls)
    logger.debug('Container created')

    return container
