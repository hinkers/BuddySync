api1 = {
    'auth_type': 'apikey',
    'api_key': '$API_KEY',
    'apikey_name': 'token',
    'apikey_location': 'param',
    'base_url': 'https://example.com',
    'endpoints': []
}

endpoint_top_headlines = {
    'name': 'top_headlines',
    'endpoint': '/top-headlines',
    'method': 'GET'
}

endpoint_search1 = {
    'name': 'search',
    'endpoint': '/search',
}

endpoint_search2 = {
    'name': 'search',
    'endpoint': '/search',
    'method': 'GET',
    'params': [
        {
            'name': 'q',
            'value': 'example'
        },
        {
            'name': 'max',
            'value': '5'
        }
    ]
}
