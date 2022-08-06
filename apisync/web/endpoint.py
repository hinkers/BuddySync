import json
from dataclasses import dataclass

import requests
from apisync.container import Container
from apisync.scripts.custom_script import CustomScript
from apisync.scripts.variables import initialize_variable


@dataclass
class Endpoint:

    name: str
    endpoint: str
    method: str
    script: CustomScript
    params: dict
    headers: dict
    retry_count: int
    api: None
    container: Container

    def __init__(self, name, container, Endpoint, Script, Method='GET', **kwargs):
        self.name = name
        self.container = container
        self.endpoint = Endpoint
        self.script = CustomScript(Script, container)
        self.method = Method
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
        self.dict = initialize_variable(self.container.variables, self.dict)

    def send_request(self):
        self.retry_count = 0
        kwargs = dict(
            params=self.api.params(self.params),
            headers=self.api.headers(self.headers)
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

    def run(self):
        response = self.send_request()
        loc = dict(
            response=response,
            raw=response.raw,
            variables=self.container.variables,
            success=False
        )
        try:
            loc['data'] = response.json()
        except requests.JSONDecodeError:
            loc['data'] = None
        self.script.run(loc)
