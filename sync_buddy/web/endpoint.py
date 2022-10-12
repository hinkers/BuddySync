import json
from dataclasses import dataclass

import requests
from sync_buddy.scripts.variables import initialize_variable


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

    def __init__(self, container, api, endpoint, method='GET', name='default', **kwargs):
        self.api = api
        self.name = name
        self.container = container
        self.endpoint = endpoint
        self.method = method
        self.params = dict()
        self.headers = dict()
        self.data = dict()
        self.putfile = None
        self.retry_count = 0

        for key, value in kwargs.items():
            if key.lower().startswith('param_'):
                self.params[key[6:]] = value
            elif key.lower().startswith('header_'):
                self.headers[key[6:]] = value
            elif key.lower() == 'data':
                self.data = json.loads(value)
            elif key.lower() == 'datafile':
                with open(value, 'r') as datafile:
                    self.data = json.load(datafile)
            elif key.lower() == 'putfile':
                self.putfile = value

        self.validate()
        self.initialize_variables()

    def validate(self):
        assert self.method in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'), f'Unknown http method "{self.method}"'
        return True

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
        if self.method == 'PUT' and self.putfile is not None:
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
