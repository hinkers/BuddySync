from sync_buddy.web.pagination.boolean import BooleanPagination
from sync_buddy.web.pagination.max_count import MaxCountPagination
from sync_buddy.web.pagination.page_count import PageCountPagination


class Pagination:

    sub_type: str
    _params: dict
    _headers: dict
    _endpoint: object
    _full_response: bool

    def __init__(self, sub_type, *args, **kwargs):
        self.sub_type = sub_type
        self._params = dict()
        self._headers = dict()
        for key, value in kwargs.items():
            if key.startswith('Param_'):
                self.params[key[6:]] = value
            elif key.startswith('Header_'):
                self.headers[key[7:]] = value

    def __iter__(self):
        # setup
        return self

    def __next__(self):
        # return
        if self.has_next_page():
            self.setup_next_page()
            return self.return_page()
        raise StopIteration

    def has_next_page(self):
        return False

    def post_request_check(self, response):
        pass

    def setup_next_page(self):
        pass

    def return_page(self):
        response = self._endpoint.run()
        self.post_request_check(response)
        if not self._full_response:
            return response['data']
        return response

    def params(self, params):
        return { **self._params, **params }

    def headers(self, headers):
        return { **self._headers, **headers }

    def pages(self, endpoint, full_response=False):
        self._endpoint = endpoint
        self._full_response = full_response
        return self


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
