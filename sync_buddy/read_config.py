from sys import getsizeof
from typing import List

import hiyapyco
from dotenv import dotenv_values

from container import Container
from sync_buddy.logger import get_logger
from sync_buddy.web.schema import validate_web


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
    web_data = validate_web(config['api'])

    # container = Container(web_data)
    container = Container(config)

    logger.info('Finished reading config, valid')
    return container
