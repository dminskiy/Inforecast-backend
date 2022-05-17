class DataColumn:
    def __init__(self, col, dtype):
        self._col = col
        self._dtype = dtype


class DataCell(DataColumn):
    def __init__(self, col: str, dtype, is_cumulative: bool):
        super(DataCell, self).__init__(col=col, dtype=dtype)
        self._val = None
        self.is_cumulative = is_cumulative

    def col(self):
        return self._col

    def set_val(self, val):
        assert type(val) == self._dtype, f'Cannot set value, wrong type: {type(val)}.' \
                                         f'\nRequired: {self._dtype}'
        self._val = val

    def get_val(self):
        return self._val

    def type(self):
        return self._dtype

