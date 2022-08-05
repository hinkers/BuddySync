import json
from dataclasses import dataclass

import requests
from apisync.container import Container
from apisync.scripts.custom_script import CustomScript
from apisync.scripts.variable import Variable


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

        self.validate()
        self.initialize_variables()

    def validate(self):
        assert self.method in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'), f'Unknown http method "{self.method}"'
        return True

    def initialize_variables(self):
        if self.container.variables.contains_variable(self.endpoint):
            self.endpoint = Variable(self.endpoint, self.container.variables)

        for param in self.params:
            if self.container.variables.contains_variable(self.params[param]):
                self.params[param] = Variable(self.params[param], self.container.variables)

        for header in self.headers:
            if self.container.variables.contains_variable(self.headers[header]):
                self.headers[header] = Variable(self.headers[header], self.container.variables)

    def send_request(self):
        self.retry_count = 0
        response = requests.request(
            self.method,
            self.api.url(self.endpoint),
            params=self.api.params(self.params),
            headers=self.api.headers(self.headers),
            json=self.data
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
