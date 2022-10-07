from rauth import OAuth1Service as OAuth1ServiceBase

from sync_buddy.web.oauth.web_server import webserver_for_code


class OAuth1Service(OAuth1ServiceBase):

    def do_authorize_token(self):
        request_token, request_token_secret = self.get_request_token()
        authorize_url = self.get_authorize_url(request_token)
        print(authorize_url)
        pin = input('PIN:')
        return self.get_auth_session(
            request_token,
            request_token_secret,
            method='POST',
            data={'oauth_verifier': pin}
        )

    def handle_http(self, endpoint, response):
        return response
