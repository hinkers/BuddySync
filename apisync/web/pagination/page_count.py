from apisync.web.pagination.pagination import Pagination


class PageCountPagination(Pagination):
    
    def __init__(self, sub_type, *args, **kwargs):
        super().__init__(sub_type, *args, **kwargs)
