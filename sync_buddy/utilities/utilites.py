from sync_buddy.utilities.map_to import map_to

class Utilities:

    _container: object
    map_to = map_to

    def __init__(self, container):
        self._container = container
