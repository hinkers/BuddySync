import json
import os
from base64 import b64decode, b64encode

import requests
from apisync.web.endpoint import Endpoint
from apisync.web.oauth.web_server import webserver_for_code
from rauth import OAuth2Service as OAuth2ServiceBase


class OAuth2Service(OAuth2ServiceBase):

    temp_webserver: bool
    redirect_uri: str
    response_type: str
    scope: str
    access_token: str
    refresh_token: str
    attempt_local: bool

    def __init__(self, *args, **kwargs):
        self.access_token = None
        self.refresh_token = None
        self.attempt_local = False
        self.temp_webserver = False
        if 'response_type' in kwargs:
            self.response_type = kwargs.get('response_type')
            del kwargs['response_type']
        if 'scope' in kwargs:
            self.redirect_uri = kwargs.get('scope')
            del kwargs['scope']
        if 'redirect_uri' in kwargs:
            self.redirect_uri = kwargs.get('redirect_uri')
            del kwargs['redirect_uri']
        if 'temp_webserver' in kwargs:
            self.temp_webserver = True if kwargs['temp_webserver'] == 'True' else False
            del kwargs['temp_webserver']
        if self.read_tokens():
            self.attempt_local = True
        return super().__init__(*args, **kwargs)

    def read_tokens(self):
        try:
            with open('.auth', 'r') as token_file:
                tokens = json.loads(b64decode(token_file.read()))
                self.access_token = tokens.get('access_token', None)
                self.refresh_token = tokens.get('refresh_token', None)
        except Exception:
            os.remove('.auth')
        return self.access_token is not None and self.read_tokens is not None

    def write_tokens(self, oauth_session):
        with open('.auth', 'w+') as token_file:
            token_file.write(b64encode(oauth_session.access_token_response.text.encode('ascii')).decode('ascii'))

    def do_authorize_token(self):
        local = self.do_local_token()
        if local is not None:
            return local

        auth_params = dict(
            response_type=self.response_type,
            redirect_uri=self.redirect_uri
        )
        if self.scope is not None:
            auth_params['scope'] = self.scope
        authorize_url = self.oauth.get_authorize_url(**auth_params)
        print(authorize_url)

        if self.temp_webserver:
            code = webserver_for_code(self.redirect_uri)
        else:
            code = input('code:')

        d_data = dict(
            code=code,
            grant_type='authorization_code',
            redirect_uri=self.redirect_uri
        )
        oauth_session = self.get_auth_session(data=d_data, decoder=json.loads)

        if 'refresh_token' in self.access_token_response.json():
            self.refresh_token = self.access_token_response.json().get('refresh_token')

        self.write_tokens(oauth_session)
        return oauth_session

    def do_refresh_token(self):
        d_data = dict(
            refresh_token=self.refresh_token,
            grant_type='refresh_token',
            redirect_uri=self.redirect_uri
        )
        oauth_session = self.get_auth_session(data=d_data, decoder=json.loads)
        self.write_tokens(oauth_session)
        return oauth_session

    def do_local_token(self):
        if not self.attempt_local:
            return None
        return self.get_session(self.access_token)

    def handle_http(self, endpoint: Endpoint, response: requests.Response):
        if response.status_code == 401:
            if endpoint.retry_count == 0:
                self.do_refresh_token()
                return endpoint.retry()
            elif endpoint.retry_count == 1:
                self.do_authorize_token()
                return endpoint.retry()
            else:
                raise Exception
        return response
