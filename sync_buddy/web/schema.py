from enum import Enum
import re

from schema import And, Optional, Or, Regex, Schema, Use


class AuthType(Enum):
    NONE = 'none'
    APIKEY = 'apikey'
    OAUTH1 = 'oauth1'
    OAUTH2 = 'oauth2'
    CUSTOM = 'custom'


class Method(Enum):
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'
    PUT = 'put'
    DELETE = 'delete'


class Location(Enum):
    PARAM = 'param'
    HEADER = 'header'


class Pagination(Enum):
    CUSTOM = 'custom'
    BOOLEAN = 'boolean'
    MAX_COUNT = 'max_count'
    PAGE_COUNT = 'page_count'


optional_params = {
    Optional('params'): [{
        'name': And(str, len),
        'value': Use(str),
    }]
}
optional_headers = {
    Optional('headers'): [{
        'name': And(str, len),
        'value': Use(str),
    }]
}


def validate_api(data):
    VALID_URL = Regex(
        '(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])',
        flags=re.IGNORECASE
    )

    required_fields = {
        Optional('name'): And(str, len),
        'auth_type': And(str, Use(str.lower), Or(*[e.value for e in AuthType])),
        'base_url': VALID_URL,
        'endpoints': [{
            'name': And(str, len),
            'method': And(str, Use(str.lower), Or(*[e.value for e in Method])),
            'endpoint': And(str, len),
            Optional('data'): And(str, len),
            Optional('data_file'): And(str, len),
            Optional('put_file'): And(str, len),
            **optional_params,
            **optional_headers
        }],
    }

    data = Schema({
        object: object,  # Get all extra keys
        **required_fields
    }).validate(data)

    # Validate API key authentication
    if data['auth_type'] == AuthType.APIKEY.value:
        return Schema({
            'api_key': And(str, len),
            'apikey_name': And(str, len),
            'apikey_location': And(str, Use(str.lower), Or(*[e.value for e in Location])),
            **required_fields
        }).validate(data)

    # Validate OAuth1 authentication
    elif data['auth_type'] == AuthType.OAUTH1.value:
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
    elif data['auth_type'] == AuthType.OAUTH2.value:
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


def validate_apis(data):
    return Schema([Use(validate_api)]).validate(data)


def validate_pagination(data):
    # TODO: Finish for all pagination types and variables
    return Schema({
        Optional('name'): And(str, len),
        'type': And(str, Use(str.lower), Or(*[e.value for e in Pagination])),
        'variable_name': And(str, len),
        'variable_location': And(str, Use(str.lower), Or(*[e.value for e in Location])),
        Optional('sleep'): Use(int),
        **optional_params,
        **optional_headers,
        object: object
    }).validate(data)


def validate_paginations(data):
    return Schema([Use(validate_pagination)]).validate(data)
