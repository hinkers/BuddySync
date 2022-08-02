import json

from rauth import OAuth2Service as OAuth2ServiceBase
from web_server import webserver_for_code


class OAuth2Service(OAuth2ServiceBase):

    temp_webserver: bool
    redirect_uri: str
    refresh_token: str

    def __init__(self, *args, **kwargs):
        self.temp_webserver = False
        if 'redirect_uri' in kwargs:
            self.redirect_uri = kwargs.get('redirect_uri')
            del kwargs['redirect_uri']
        if 'temp_webserver' in kwargs:
            self.temp_webserver = True if kwargs['temp_webserver'] == 'True' else False
            del kwargs['temp_webserver']
        return super().__init__(*args, **kwargs)

    def do_authorize_token(self):
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

        return oauth_session

    def do_refresh_token(self):
        d_data = dict(
            refresh_token=self.refresh_token,
            grant_type='refresh_token',
            redirect_uri=self.redirect_uri
        )
        return self.get_auth_session(data=d_data, decoder=json.loads)
