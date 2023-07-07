import requests
from sync_buddy.web.endpoint import Endpoint
from sync_buddy.web.oauth.OAuth1Service import OAuth1Service
from sync_buddy.web.oauth.OAuth2Service import OAuth2Service
from sync_buddy.web.schema import AuthType, Location


class Api:
    auth_type: str
    base_url: str
    api_key = None
    apikey_location = None
    apikey_name = None
    oauth = None
    oauth_session = None

    def __init__(self, auth_type, base_url, **kwargs):
        self.auth_type = auth_type
        self.base_url = base_url

        if auth_type == AuthType.APIKEY.value:
            self.api_key = kwargs.get('api_key')
            self.apikey_location = kwargs['apikey_location']
            self.apikey_name = kwargs['apikey_name']
        elif auth_type in (AuthType.OAUTH1.value, AuthType.OAUTH2.value):
            self._register_oauth(auth_type, kwargs)

    def _register_oauth(self, auth_type, kwargs):
        if auth_type == AuthType.OAUTH1.value:
            self.oauth = OAuth1Service(
                consumer_key=kwargs.get('consumer_key'),
                consumer_secret=kwargs.get('consumer_secret'),
                name=kwargs.get('name'),
                access_token_url=kwargs.get('access_token_url'),
                authorize_url=kwargs.get('authorize_url'),
                request_token_url=kwargs.get('request_token_url'),
                base_url=kwargs.get('base_url')
            )
        elif auth_type == AuthType.OAUTH2.value:
            self.oauth = OAuth2Service(
                client_id=kwargs.get('client_id'),
                client_secret=kwargs.get('client_secret'),
                name=kwargs.get('name'),
                authorize_url=kwargs.get('authorize_url'),
                access_token_url=kwargs.get('access_token_url'),
                base_url=kwargs.get('base_url'),
                temp_webserver=kwargs.get('temp_webserver', False),
                redirect_uri=kwargs.get('redirect_uri'),
                response_type=kwargs.get('response_type', 'code'),
                scope=kwargs.get('scope', None)
            )

        self.oauth_session = self.oauth.do_authorize_token()

    def url(self, endpoint):
        return f'{self.base_url}{endpoint}'

    def params(self, params):
        if self.apikey_location == 'param':
            return { self.param_name: self.api_key, **params }
        return params

    def headers(self, headers):
        if self.apikey_location == 'header':
            return { self.header_name: self.api_key, **headers }
        return headers

    def handle_http(self, endpoint: Endpoint, response: requests.Response):
        if response.ok:
            return response
        if self.oauth is not None:
            return self.oauth.handle_http(endpoint, response)
        return response

    @property
    def request(self):
        if self.oauth_session is not None:
            return self.oauth_session.request
        return requests.request
