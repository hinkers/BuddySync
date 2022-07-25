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

    def run(self, auth):
        response = requests.request(self.method,
            auth.url(self.endpoint),
            params=auth.params(self.params),
            headers=auth.headers(self.headers),
            json=self.data
        )
        loc = dict(
            response=response,
            data=response.json(),
            success=False
        )
        self.script.run(loc)
