import requests
from rauth import OAuth1Service, OAuth2Service


class Api:
    auth_type: str
    base_url: str
    api_key = None
    param_name = None
    oauth = None
    oauth_session = None

    def __init__(self, AuthType, BaseUrl, **kwargs):
        self.auth_type = AuthType
        self.base_url = BaseUrl

        if AuthType == 'ApiKey':
            self.api_key = kwargs.get('ApiKey')
            self.param_name = kwargs.get('ParamName')
        elif AuthType.startswith('OAuth'):
            if AuthType == 'OAuth1':
                self.oauth = OAuth1Service(
                    consumer_key=kwargs.get('ConsumerKey'),
                    consumer_secret=kwargs.get('ConsumerSecret'),
                    name=kwargs.get('Name'),
                    access_token_url=kwargs.get('AccessTokenUrl'),
                    authorize_url=kwargs.get('AuthorizeUrl'),
                    request_token_url=kwargs.get('RequestTokenUrl'),
                    base_url=kwargs.get('BaseUrl')
                )
            elif AuthType == 'OAuth2':
                self.oauth = OAuth2Service(
                    client_id=kwargs.get('ClientId'),
                    client_secret=kwargs.get('ClientSecret'),
                    name=kwargs.get('Name'),
                    authorize_url=kwargs.get('AuthorizeUrl'),
                    access_token_url=kwargs.get('AccessTokenUrl'),
                    base_url=kwargs.get('BaseUrl')
                )
            authorize_url = self.oauth.get_authorize_url(
                scope=kwargs.get('Scope'),
                response_type=kwargs.get('ResponseType'),
                redirect_uri=kwargs.get('RedirectUrl')
            )
            print(authorize_url)
            redirect_uri = authorize_url
            self.oauth_session = self.oauth.get_auth_session(data=dict(
                code=input('code:'),
                redirect_uri=redirect_uri
            ))

    def url(self, endpoint):
        return f'{self.base_url}{endpoint}'

    def params(self, params):
        if self.param_name is not None:
            return { self.param_name: self.api_key, **params }
        return params

    def headers(self, headers):
        return { **headers }

    @property
    def request(self):
        if self.oauth_session is not None:
            return self.oauth_session.request
        return requests.request
