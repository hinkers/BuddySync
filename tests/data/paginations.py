pagination_max_count = {
    'name': 'max_count',
    'type': 'max_count',
    'variable_name': 'page',
    'variable_location': 'PARAM',
    'total_json_path': 'totalArticles',
    'count_json_path': 'articles.`len`',
    'params': [
        {'name': 'query', 'value': '10 cats'}
    ],
    'headers': [
        {'name': min, 'value': 100},
        {'name': max, 'value': 100}
    ],
    'sleep': 1
}
