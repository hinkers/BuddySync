from sync_buddy.web.pagination.pagination import Pagination


class MaxCountPagination(Pagination):
    
    def __init__(self, sub_type, *args, **kwargs):
        super().__init__(sub_type, *args, **kwargs)
