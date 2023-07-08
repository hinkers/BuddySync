from sync_buddy.container import Container
from sync_buddy.read_config import read_config


def test_container_apis():
    container = read_config('tests/data/test_configs/.env',
    [
        'tests/data/test_configs/apis.yaml',
        'tests/data/test_configs/paginations.yaml',
        'tests/data/test_configs/scripts.yaml',
        'tests/data/test_configs/databases.yaml',
        'tests/data/test_configs/variables.yaml',
    ])

    assert isinstance(container, Container)

