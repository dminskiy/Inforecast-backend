from InforecastDataStructs import DataColumn, SupportedDataTypes


class Columns:
    def __init__(self):
        self._columns = {}

    def add_column(self, ppty: DataColumn):
        ppty_name = ppty.get_name()
        ppty_tag = ppty.get_tag()
        assert ppty_tag not in self._columns.keys(), f'Property with this tag already exists.\n' \
                                                     f'Tag: {ppty_tag}\nName: {ppty_name}'
        self._columns[ppty_tag](ppty)

    def to_list(self):
        return [self._columns[key].col() for key in self._columns.keys()]

    def to_dict(self):
        out_dict = {}
        for key in self._columns.keys():
            out_dict[key] = self._columns[key].get_val()

        return out_dict


class Rows:
    def __init__(self):
        # ind: [vals].
        self.rows_buffer = {}

    def val_isValid(self, val, col: DataColumn):
        if val is None or SupportedDataTypes(type(val)) == col.get_type():
            return True
        else:
            return False

    def get_row_from_table(self, ind: int):
        pass

    def get_rows_from_table(self, ind: ()):
        pass
