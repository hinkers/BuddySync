import re

from schema import And, Optional, Or, Regex, Schema, Use


def validate_api(data):
    VALID_URL = Regex(
        '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])',
        flags=re.IGNORECASE
    )

    required_fields = {
        Optional('name'): And(str, len),
        'auth_type':  And(str, Use(str.lower), Or('none', 'apikey', 'oauth1', 'oauth2')),
        'base_url': VALID_URL,
        'endpoints': [{
        'name': And(str, len),
        'method': And(str, Use(str.lower), Or('get', 'post', 'patch', 'put', 'delete')),
        'endpoint': And(str, len),
            Optional('data'): And(str, len),
            Optional('data_file'): And(str, len),
            Optional('params'): [{
                'name': And(str, len),
                'value': Use(str),
            }]
        }],
    }

    data = Schema({
        object: object,  # Get all extra keys
        **required_fields
    }).validate(data)

    # Validate API key authentication
    if data['auth_type'] == 'apikey':
        return Schema({
            'api_key': And(str, len),
            'apikey_name': And(str, len),
            'apikey_location': And(str, Use(str.lower), Or('param', 'header')),
            **required_fields
        }).validate(data)

    # Validate OAuth1 authentication
    elif data['auth_type'] == 'oauth1':
        return Schema({
            'consumer_key': And(str, len),
            'consumer_secret': And(str, len),
            'name': And(str, len),
            'authorize_url': VALID_URL,
            'access_token_url': VALID_URL,
            'request_token_url': VALID_URL,
            **required_fields
        }).validate(data)

    # Validate OAuth2 authentication
    elif data['auth_type'] == 'oauth2':
        return Schema({
            'client_id': And(str, len),
            'client_secret': And(str, len),
            'name': And(str, len),
            'redirect_url': VALID_URL,
            'authorize_url': VALID_URL,
            'access_token_url': VALID_URL,
            Optional('response_type'): And(str, len),
            Optional('temp_web_server'): bool,
            **required_fields
        }).validate(data)


def validate_web(data):
    return Schema([Use(validate_api)]).validate(data)
