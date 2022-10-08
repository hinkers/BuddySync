from time import sleep
from sync_buddy.web.pagination.page_tracker import PageTracker


class Pagination:

    sub_type: str
    _params: dict
    _headers: dict
    _endpoint: object
    _full_response: bool
    _page_tracker: object

    def __init__(self, *args, **kwargs):
        self._page_tracker = PageTracker(*args, **kwargs)
        self._params = dict()
        self._headers = dict()
        self._sleep = int(kwargs.get('Sleep', 0))
        for key, value in kwargs.items():
            if key.startswith('Param_'):
                self._params[key[6:]] = value
            elif key.startswith('Header_'):
                self._headers[key[7:]] = value

    def __iter__(self):
        # setup
        self.reset()
        self._page_tracker.reset()
        return self

    def __next__(self):
        if self.has_next_page():
            if self._page_tracker.not_first() and self._sleep > 0:
                sleep(self._sleep)
            page = self.return_page()
            self.setup_next_page()
            return page
        raise StopIteration

    def reset(self):
        pass

    def has_next_page(self):
        return False

    def after_request_check(self, response):
        pass

    def setup_next_page(self):
        self._page_tracker.increment()

    def return_page(self):
        response = self._endpoint.run(self.params(), self.headers())
        self.after_request_check(response)
        if not self._full_response:
            return response['data']
        return response

    def params(self):
        return { **self._params, **self._page_tracker.params() }

    def headers(self):
        return { **self._headers, **self._page_tracker.headers() }

    def pages(self, endpoint, full_response=False):
        self._endpoint = endpoint
        self._full_response = full_response
        return self

