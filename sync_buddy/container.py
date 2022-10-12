import re

from sync_buddy.database.sql import SQL
from sync_buddy.logger import get_logger
from sync_buddy.scripts.custom_script import CustomScript
from sync_buddy.scripts.variables import Variables, load_variables, save_variables
from sync_buddy.utilities.utilites import Utilities
from sync_buddy.web.api import Api
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.pagination.factory import create_pagination


class GenericObject:

    def __init__(self, _dict):
        for name, value in _dict.items():
            setattr(self, camel_to_snake(name), value)


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def name(d):
    return d.get('name', 'default')


class Container:

    variables: Variables
    auth: object()
    endpoints: dict()
    sqls: object()
    scripts: dict()
    run: dict()
    paginations: dict()

    def __init__(self, config):
        logger = get_logger('app')

        self.variables = Variables()
        self.endpoints = dict()
        self.paginations = dict()
        self.sqls = dict()
        self.utilities = Utilities(self)

        # Load APIs and Endpoints
        for api_definition in config['api']:
            api = Api(**api_definition)

            for endpoint_definition in api_definition['endpoints']:
                endpoint_name = name(endpoint_definition)
                if endpoint_name in self.endpoints:
                    logger.warning(f'Overriding duplicate endpoint "{endpoint_name}"')

                self.endpoints[endpoint_name] = Endpoint(self, api, **endpoint_definition)
            logger.debug(f'Loaded {len(self.endpoints)} Endpoint definitions')
        logger.debug(f'Loaded {len(config["api"])} API definitions')

        # Load Paginations
        for pagination_definition in config['pagination']:
            self.paginations[name(pagination_definition)] = create_pagination(**pagination_definition)
        logger.debug(f'Loaded {len(self.paginations)} Pagination definitions')

        # Load SQL
        for sql_definition in config['sql']:
            sql = SQL(**sql_definition)

            for table_definition in sql_definition['table']:
                sql.add_table(**table_definition)
            logger.debug(f'Loaded {len(sql.tables)} table definitions')

            for type_, relations in sql_definition['relationship'].items():
                sql.add_relationships(type_, relations)
            logger.debug(f'Loaded {len(sql.relationships)} relationships')  
          
            self.sqls[name(sql_definition)] = sql
        logger.debug(f'Loaded {len(self.sqls)} SQL definitions')
        
        # Load Scripts
        self.scripts = [CustomScript(self, filepath) for filepath in config['run']]
        logger.debug(f'Loaded {len(self.scripts)} total scripts')

        # Load vriables
        self.variables.load_variables(**config['variable'])
        self.load_variables()
        logger.debug(f'Config variables updated')

    def load_variables(self):
        load_variables(self.variables)

    def save_variables(self):
        save_variables(self.variables)

    def endpoints_as_object(self):
        return GenericObject(self.endpoints)

    def pagination_as_object(self):
        return GenericObject({n: p.pages for n, p in self.paginations.items()})
