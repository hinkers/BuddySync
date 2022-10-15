from typing import Any
from xml.dom import ValidationErr
from jsonpath_ng.ext import parse
from sync_buddy.web.pagination.pagination import Pagination


class MaxCountPagination(Pagination):
    
    _has_next_page: bool
    _total_results: int
    _results_count: int
    _total_type: str
    _count_type: str
    _jsonpath_total: Any
    _jsonpath_count: Any
    _header_total: str
    _header_count: str

    def __init__(self, *args, **kwargs):
        if 'total_json_path' in kwargs:
            self._total_type = 'json'
            self._jsonpath_total = parse(kwargs['total_json_path'])
        elif 'total_header' in kwargs:
            self._total_type = 'header'
            self._header_total = kwargs['total_header']

        if 'count_json_path' in kwargs:
            self._count_type = 'json'
            self._jsonpath_count = parse(kwargs['count_json_path'])
        elif 'count_header' in kwargs:
            self._total_type = 'header'
            self._header_total = kwargs['count_header']

        super().__init__(*args, **kwargs)

    def reset(self):
        self._total_results = 0
        self._results_count = 0
        self._has_next_page = True

    def update_total(self, response):
        if self._total_type == 'json':
            total_matches = self._jsonpath_total.find(response['data'])
            if len(total_matches) > 0:
                self._total_results = int(total_matches[0].value)
        elif self._total_type == 'header':
            response['response'].headers[self._header_total]

    def update_count(self, response):
        if self._count_type == 'json':
            count_matches = self._jsonpath_count.find(response['data'])
            if len(count_matches) > 0:
                self._results_count = int(count_matches[0].value)
        elif self._count_type == 'header':
            response['response'].headers[self._header_count]

    def after_request_check(self, response):
        self._has_next_page = False

        self.update_total(response)
        self.update_count(response)

        if self._results_count < self._total_results:
            self._has_next_page = True

    def has_next_page(self):
        return self._has_next_page
