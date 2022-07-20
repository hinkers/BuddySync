import requests
from dataclasses import dataclass
from datetime import datetime as dt

def datetime(d_str, s_format=None):
    return dt.strptime(d_str, s_format if s_format is not None else '%Y-%m-%d %H:%M:%S')

@dataclass
class Endpoint:
    name: str
    endpoint: str
    method: str
    script: str

    def __init__(self, name, endpoint, script, method='GET'):
        self.name = name
        self.endpoint = endpoint
        self.script = script
        self.method = method

    def validate(self):
        assert self.method in ('GET', 'POST', 'PATCH', 'PUT', 'DELETE'), f'Unknown http method "{self.method}"'
        return True

    def run(self, auth, session, tables):
        if self.method == 'GET':
            response = requests.get(auth.url(self.endpoint), params=auth.params())
            loc = dict(
                response=response,
                data=response.json(),
                Session=session,
                success=False,
                datetime=datetime,
                **tables
            )
            with open(self.script, 'r') as script:
                exec(compile(script.read(), self.script, 'exec'), dict(), loc)
