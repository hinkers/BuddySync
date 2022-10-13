from sync_buddy.web.pagination.boolean import BooleanPagination
from sync_buddy.web.pagination.page_count import PageCountPagination
from sync_buddy.web.pagination.max_count import MaxCountPagination
from sync_buddy.web.pagination.pagination import Pagination
from sync_buddy.web.schema import Pagination as PaginationEnum


def create_pagination(type, *args, **kwargs) -> Pagination:
    mapping = {
        PaginationEnum.CUSTOM.value: Pagination,
        PaginationEnum.BOOLEAN.value: BooleanPagination,
        PaginationEnum.MAX_COUNT.value: MaxCountPagination,
        PaginationEnum.PAGE_COUNT.value: PageCountPagination,
    }

    return mapping[type](*args, **kwargs)
