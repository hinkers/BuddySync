from dataclasses import dataclass

@dataclass
class Authentication:
    auth_type: str
    api_key: str
    param_name: str
    base_url: str

    def __init__(self, authtype, apikey, paramname, baseurl):
        self.auth_type = authtype
        self.api_key = apikey
        self.param_name = paramname
        self.base_url = baseurl
    
    def url(self, endpoint):
        return f'{self.base_url}{endpoint}'

    def params(self):
        return { self.param_name: self.api_key }