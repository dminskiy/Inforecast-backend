import pandas as pd
import os


class Table:
    def __init__(self):
        self._table = None
        self._cols_list = None
        self._index = None

    def create_table(self, columns: list, index: str = None):
        assert len(columns) > 0
        assert type(columns[0]) is str, f'List of strings is expected as input. Got: {columns[0].type}'
        self._table = pd.DataFrame(columns=columns)
        self._index = index
        if index:
            self._table.set_index(self._index)
        self._cols_list = columns

    def save_table(self, table_path: str, table_name: str):
        if not os.path.exists(table_path):
            os.makedirs(table_path)

        if not table_name.endswith('.csv'):
            table_name += '.csv'

        full_path = os.path.join(table_path, table_name)
        # TODO: check if name exists, rename if it does
        self._table.to_csv(full_path)

    def load_table(self, table_path: str, table_name: str):
        table_full_path = os.path.join(table_path, table_name)
        assert table_name.endswith('.csv'), f'Table name needs to be .csv\nReceived: {table_name}'
        assert os.path.exists(table_full_path)

        self._table = pd.read_csv(table_full_path)
        self._cols_list = list(self._table)

    def insert_row(self, new_row: dict):
        assert self._table is not None
        row_cols = list(new_row.keys())
        assert row_cols.sort() == self._cols_list.sort()

        if self._index:
            assert self._index in new_row.keys(), 'Table index not found in the row being inserted'
            index = new_row[self._index]
            del new_row[self._index]
            row_df = pd.DataFrame(new_row, index=[index])
        else:
            row_df = pd.DataFrame(new_row, index=[0])

        self._table = pd.concat([self._table, row_df], ignore_index=False)

    def get_column_list(self):
        return self._cols_list

    def get_index_name(self):
        return self._table.index

    def get_value(self, indx, col: str):
        return self._table.at[indx, col]

    def set_value(self, indx, col: str, val):
        self._table.at[indx, col] = val


if __name__ == '__main__':
    from random import randint

    cols = ['col1', 'col2', 'col3', 'col4']

    rows = []
    for i in range(10):
        row = {}
        row['ind'] = i
        for col in cols:
            row[col] = randint(0, 10000)
        rows.append(row)

    table = Table()
    cols += ['ind']
    table.create_table(columns=cols, index='ind')

    for row in rows:
        table.insert_row(row)

    table.set_value(indx=5, col='col2', val='CHANGED')

    table.save_table(table_path='../test_dir', table_name='DataHandler_test_table.csv')
