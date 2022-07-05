from Table import Table
from enum import Enum
from typing import Dict
from DataColumn import DataColumn


class ValidationTableRows(Enum):
    NAME = 0
    DTYPE = 1
    LIM_MIN = 2
    LIM_MAX = 3


class InforecastValidationTable(Table):
    def __init__(self):
        super(InforecastValidationTable, self).__init__()
        # incex col name for the validation table
        self.val_ind: str = 'index'
        self.next_ind_val: int = 0
        # max from ValidationTableRows
        self.pre_options_val_ind: int = 4

    def init(self, data_cols: Dict[str, DataColumn]):
        '''
        Initialises the table by creating a table where cols correspond to cols in the main table passed via data_cols
        and rows correspond to the key information about a column. Indexes in ValidationTableRows represent constant
        params, indexes beyond represent options for a drop-down menu
        :param data_cols: dict [str, DataColumn] <=> column tag: DataColumn object
        :return: True; False if empty data_cols; can throw RuntimeError
        '''

        if not data_cols:
            return False

        cols = list(data_cols.keys()) + [self.val_ind]
        self.create_table(columns=cols, index=self.val_ind)

        # Process main validation criteria
        for i in range(self.pre_options_val_ind):
            row = {}
            row[self.val_ind] = self.next_ind_val
            self.next_ind_val += 1
            for tag in data_cols:
                data_col = data_cols[tag]
                if i == ValidationTableRows.NAME.value:
                    row[tag] = data_col.get_name()
                elif i == ValidationTableRows.DTYPE.value:
                    row[tag] = str(data_col.get_type())
                elif i == ValidationTableRows.LIM_MIN.value:
                    if data_col.get_limit():
                        row[tag] = data_col.get_limit()[0]
                    else:
                        row[tag] = None
                elif i == ValidationTableRows.LIM_MAX.value:
                    if data_col.get_limit():
                        row[tag] = data_col.get_limit()[1]
                    else:
                        row[tag] = None
                else:
                    raise RuntimeError('Cannot init Validation Table - index out of range')

            self.insert_row(new_row=row)

        # Add options
        max_options = 0
        for tag in data_cols:
            data_col = data_cols[tag]
            if data_col.num_options > max_options:
                max_options = data_col.num_options

        for i in range(max_options):
            row = {}
            row[self.val_ind] = self.next_ind_val
            self.next_ind_val += 1

            for tag in data_cols:
                data_col = data_cols[tag]

                if i < data_col.num_options:
                    row[tag] = data_col.get_options()[i]
                else:
                    row[tag] = None

            self.insert_row(new_row=row)

        return True
