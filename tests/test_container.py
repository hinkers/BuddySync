from sync_buddy.container import Container, GenericObject, camel_to_snake, name
from sync_buddy.database.sql import SQL
from sync_buddy.database.sql_table import SqlTable
from sync_buddy.scripts.custom_script import CustomScript
from sync_buddy.scripts.variables import Variables
from sync_buddy.web.api import Api
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.pagination.pagination import Pagination

from .data.apis import (api1, endpoint_search1, endpoint_search2,
                        endpoint_top_headlines)
from .data.paginations import pagination_max_count
from .data.sqls import sql1


class TestFunctions:
    def test_camel_to_snake(self):
        assert camel_to_snake('HelloWorld') == 'hello_world'
        assert camel_to_snake('CamelCase') == 'camel_case'
        assert camel_to_snake('CamelCamelCase') == 'camel_camel_case'
        assert camel_to_snake('Camel2Camel2Case') == 'camel2_camel2_case'
        assert camel_to_snake('getHTTPResponseCode') == 'get_http_response_code'
        assert camel_to_snake('get2HTTPResponseCode') == 'get2_http_response_code'
        assert camel_to_snake('get2HTTPResponse123Code') == 'get2_http_response123_code'
        assert camel_to_snake('HTTPResponseCode') == 'http_response_code'
        assert camel_to_snake('HTTPResponseCodeXYZ') == 'http_response_code_xyz'

    def test_name(self):
        assert name({}) == 'default'
        assert name({'name': 'default'}) == 'default'
        assert name({'name': 'Jerry'}) == 'Jerry'
        assert name({'name': 'Albert'}) == 'Albert'


class TestGenericObject:
    def test_generic_object_snake(self):
        go = GenericObject({'Name': 'default', 'Value': 3})
        assert isinstance(go, GenericObject)
        assert getattr(go, 'name', None) == 'default'
        assert isinstance(getattr(go, 'value', None), int)
        assert getattr(go, 'value') == 3

    def test_generic_object_came_case(self):
        go = GenericObject({'Name': 'default', 'Value': 3}, to_snake=False)
        assert isinstance(go, GenericObject)
        assert getattr(go, 'Name', None) == 'default'
        assert isinstance(getattr(go, 'Value', None), int)
        assert getattr(go, 'Value') == 3


class TestContainer:
    def test_container_empty(self):
        assert isinstance(Container(), Container)

    def test_container_apis(self):
        api = api1
        api['endpoints'].append(endpoint_top_headlines)
        api['endpoints'].append(endpoint_search1)
        api['endpoints'].append(endpoint_search2)
        apis = [api]        

        container = Container(apis=apis)

        assert len(container.endpoints) == 2
        for endpoint in container.endpoints.values():
            assert isinstance(endpoint, Endpoint)
            assert isinstance(endpoint.api, Api)
            assert endpoint.container is container
        assert len(container.endpoints['search'].params) == 2

    def test_container_paginations(self):
        container = Container(paginations=[pagination_max_count])

        assert len(container.paginations) == 1
        assert isinstance(container.paginations.get('max_count', None), Pagination)

    def test_container_sqls(self):
        container = Container(sqls=[sql1])
        
        assert len(container.sqls) == 1
        assert isinstance(container.sqls.get('default', None), SQL)
        assert len(container.sqls.get('default', None).tables) == 2
        assert issubclass(container.sqls.get('default', None).tables['News'], SqlTable)
        assert issubclass(container.sqls.get('default', None).tables['Source'], SqlTable)

    def test_container_scripts(self):
        container = Container(scripts=['scripts/my_script.py', 'scripts/test_script.py'])
        
        assert len(container.scripts) == 2
        for script in container.scripts:
            assert isinstance(script, CustomScript)

    def test_container_variables(self):
        container = Container(variables={'var1': 1, 'var2': None, 'var3': 'str'})

        assert isinstance(container.variables, Variables)
        assert len(container.variables.as_dict()) == 3
        assert len(container.variables.keys()) == 3
        assert container.variables.var1 == 1
        assert container.variables.var2 is None
        assert container.variables.var3 == 'str'
