
class PageTracker:

    _variable_name: str
    _variable_type: str
    _starting_number: int
    _increment_amount: int
    _current_page: int

    def __init__(self, *args, **kwargs):
        self._variable_name = kwargs['VariableName']
        self._variable_type = kwargs['VariableType'].lower()
        self._starting_number = kwargs.get('PageStart', 1)
        self._increment_amount = kwargs.get('PageIncrement', 1)

        self.reset()

    def increment(self, amount=None):
        if amount is None:
            amount = self._increment_amount
        self._current_page += amount

    def reset(self):
        self._current_page = self._starting_number

    def headers(self):
        if self._variable_type != 'header':
            return dict()
        return {self._variable_name: self._current_page}

    def params(self):
        if self._variable_type != 'param':
            return dict()
        return {self._variable_name: self._current_page}

    def not_first(self):
        return not (self._current_page == self._starting_number)
