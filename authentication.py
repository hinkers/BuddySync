class Authentication:
    auth_type: str
    base_url: str
    api_key = None
    param_name = None

    def __init__(self, AuthType, BaseUrl, **kwargs):
        self.auth_type = AuthType
        self.base_url = BaseUrl

        if AuthType == 'ApiKey':
            self.api_key = kwargs['ApiKey']
            self.param_name = kwargs['ParamName']

    
    def url(self, endpoint):
        return f'{self.base_url}{endpoint}'

    def params(self, params):
        if self.param_name is not None:
            return { self.param_name: self.api_key, **params }
        return params

    def headers(self, headers):
        return { **headers }
