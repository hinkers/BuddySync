from ast import Try
import json
from dataclasses import dataclass

import requests
from sqlalchemy import false

from custom_script import CustomScript


@dataclass
class Endpoint:
    name: str
    endpoint: str
    method: str
    script: CustomScript
    params: dict
    headers: dict
    auth: None

    def __init__(self, name, Endpoint, Script, Method='GET', **kwargs):
        self.name = name
        self.endpoint = Endpoint
        self.script = CustomScript(Script)
        self.method = Method
        self.params = dict()
        self.headers = dict()
        self.data = dict()

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

    def validate(self):
        assert self.method in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'), f'Unknown http method "{self.method}"'
        return True

    def request(self, *args, **kwargs):
        return self.auth.request(*args, **kwargs)

    def run(self):
        response = requests.request(self.method,
            self.auth.url(self.endpoint),
            params=self.auth.params(self.params),
            headers=self.auth.headers(self.headers),
            json=self.data
        )
        loc = dict(
            response=response,
            raw=response.raw,
            success=False
        )
        try:
            loc['data'] = response.json()
        except requests.JSONDecodeError:
            loc['data'] = None
        self.script.run(loc)
