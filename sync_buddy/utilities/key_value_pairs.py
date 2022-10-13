from typing import Any


class KVP:
    '''
    TODO: Delete
    This might not be needed anymore.
    '''

    _data: list[dict[Any, Any]]
    _current: int

    def __init__(self, data: list[dict[Any, Any]]):
        self._data = data
        self._current = 0

        raise DeprecationWarning('KVP is marked for removal')
    
    def __iter__(self):
        self._current = 0
        return self

    def __next__(self) -> tuple[Any, Any]:
        if self._current < len(self._data):
            key = next(iter(self._data[self._current]))
            value = self._data[self._current][key]
            self._current += 1
            return key, value
        raise StopIteration
