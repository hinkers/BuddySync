from sync_buddy.web.pagination.boolean import BooleanPagination
from sync_buddy.web.pagination.page_count import PageCountPagination
from sync_buddy.web.pagination.max_count import MaxCountPagination
from sync_buddy.web.pagination.pagination import Pagination


def create_pagination(Type, *args, **kwargs) -> Pagination:
    valid_types = (
        'Custom',
        'Boolean',
        'MaxCount',
        'PageCount'
    )
    assert Type in valid_types, f'Unknown pagination type "{Type}".'

    if Type == 'Boolean':
        return BooleanPagination(*args, **kwargs)
    if Type == 'MaxCount':
        return MaxCountPagination(*args, **kwargs)
    if Type == 'PageCount':
        return PageCountPagination(*args, **kwargs)
    return Pagination(*args, **kwargs)
