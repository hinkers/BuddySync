import json
from dataclasses import dataclass

import requests
from sync_buddy.scripts.variables import initialize_variable
from sync_buddy.utilities.key_value_pairs import KVP
from sync_buddy.web.schema import Method


@dataclass
class Endpoint:

    name: str
    endpoint: str
    method: str
    params: dict
    headers: dict
    _temp_params: dict
    _temp_headers: dict
    retry_count: int
    api: None
    container: object

    def __init__(self, container, api, endpoint, method=None, name='default', **kwargs):
        self.api = api
        self.name = name
        self.container = container
        self.endpoint = endpoint
        self.method = method or Method.GET
        self.params = dict()
        self.headers = dict()
        self.data = dict()
        self.putfile = None
        self.retry_count = 0

        for var in kwargs.get('params', []):
            self.params[var['name']] = var['value']
        for var in kwargs.get('headers', []):
            self.params[var['name']] = var['value']

        if 'data' in kwargs:
            self.data = json.loads(kwargs['data'])
        if 'data_file' in kwargs:
            with open(kwargs['data_file'], 'r') as datafile:
                self.data = json.load(datafile)
        if 'put_file' in kwargs:
            self.putfile = kwargs['put_file']

        self.initialize_variables()

    def initialize_variables(self):
        self.endpoint = initialize_variable(self.container.variables, self.endpoint)
        self.params = initialize_variable(self.container.variables, self.params)
        self.headers = initialize_variable(self.container.variables, self.headers)
        self.data = initialize_variable(self.container.variables, self.data)

    def send_request(self):
        self.retry_count = 0
        kwargs = dict(
            params=self.api.params({**self.params, **self._temp_params}),
            headers=self.api.headers({**self.headers, **self._temp_headers})
        )
        if self.data is not None and len(self.data) > 0:
            kwargs['json'] = self.data
        if self.method == Method.PUT and self.putfile is not None:
            with open(self.putfile, 'rb') as putfile:
                kwargs['data'] = putfile.read()
        response = requests.request(
            self.method,
            self.api.url(self.endpoint),
            **kwargs
        )
        return self.api.handle_http(self, response)

    def request(self, *args, **kwargs):
        return self.api.request(*args, **kwargs)

    def retry(self):
        self.retry_count += 1
        return self.send_request()

    def run(self, temp_params=None, temp_headers=None):
        if temp_params is None:
            temp_params = dict()
        if temp_headers is None:
            temp_headers = dict()

        self._temp_params = temp_params
        self._temp_headers = temp_headers

        response = self.send_request()
        loc = dict(
            response=response,
            raw=response.raw
        )
        try:
            loc['data'] = response.json()
        except requests.JSONDecodeError:
            loc['data'] = None
        return loc
