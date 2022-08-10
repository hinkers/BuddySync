from apisync.web.pagination.boolean import BooleanPagination
from apisync.web.pagination.max_count import MaxCountPagination
from apisync.web.pagination.page_count import PageCountPagination


class Pagination:

    sub_type: str
    _params: dict
    _headers: dict

    def __init__(self, sub_type, *args, **kwargs):
        self.sub_type = sub_type
        self._params = dict()
        self._headers = dict()
        for key, value in kwargs.items():
            if key.startswith('Param_'):
                self.params[key[6:]] = value
            elif key.startswith('Header_'):
                self.headers[key[7:]] = value

    def params(self, params):
        return { **self._params, **params }

    def headers(self, headers):
        return { **self._headers, **headers }


def create_pagination(pagination_type, sub_type, *args, **kwargs) -> Pagination:
    valid_types = (
        'Custom',
        'Boolean',
        'MaxCount',
        'PageCount'
    )
    valid_sub_types = (
        'Header',
        'JSON'
    )
    assert pagination_type in valid_types, f'Unknown pagination type "{pagination_type}".'
    assert sub_type in valid_sub_types, f'Unknown pagination sub type "{sub_type}".'

    if pagination_type == 'Boolean':
        return BooleanPagination(sub_type, *args, **kwargs)
    if pagination_type == 'MaxCount':
        return MaxCountPagination(sub_type, *args, **kwargs)
    if pagination_type == 'PageCount':
        return PageCountPagination(sub_type, *args, **kwargs)
    return Pagination(sub_type, *args, **kwargs)
