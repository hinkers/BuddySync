from sync_buddy.web.pagination.boolean import BooleanPagination
from sync_buddy.web.pagination.page_count import PageCountPagination
from sync_buddy.web.pagination.max_count import MaxCountPagination
from sync_buddy.web.pagination.pagination import Pagination


def create_pagination(type, *args, **kwargs) -> Pagination:
    valid_types = (
        'Custom',
        'Boolean',
        'MaxCount',
        'PageCount'
    )
    assert type in valid_types, f'Unknown pagination type "{type}".'

    if type == 'Boolean':
        return BooleanPagination(*args, **kwargs)
    if type == 'MaxCount':
        return MaxCountPagination(*args, **kwargs)
    if type == 'PageCount':
        return PageCountPagination(*args, **kwargs)
    return Pagination(*args, **kwargs)
