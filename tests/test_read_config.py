from sync_buddy.container import Container
from sync_buddy.read_config import read_config

from .data.paginations import pagination_max_count
from .data.databases import sql1


def test_container_apis():
    container = read_config('tests/data/test_configs/.env',
    [
        'tests/data/test_configs/apis.yaml',
        'tests/data/test_configs/paginations.yaml',
        'tests/data/test_configs/scripts.yaml',
        'tests/data/test_configs/sql.yaml',
        'tests/data/test_configs/variables.yaml',
    ])

    assert isinstance(container, Container)

