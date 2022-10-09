
class PageTracker:

    _variable_name: str
    _variable_location: str
    _starting_number: int
    _increment_amount: int
    _current_page: int

    def __init__(self, *args, **kwargs):
        self._variable_name = kwargs['variable_name']
        self._variable_location = kwargs['variable_location'].lower()
        self._starting_number = kwargs.get('page_start', 1)
        self._increment_amount = kwargs.get('page_increment', 1)

        self.reset()

    def increment(self, amount=None):
        if amount is None:
            amount = self._increment_amount
        self._current_page += amount

    def reset(self):
        self._current_page = self._starting_number

    def headers(self):
        if self._variable_location != 'header':
            return dict()
        return {self._variable_name: self._current_page}

    def params(self):
        if self._variable_location != 'param':
            return dict()
        return {self._variable_name: self._current_page}

    def not_first(self):
        return not (self._current_page == self._starting_number)
