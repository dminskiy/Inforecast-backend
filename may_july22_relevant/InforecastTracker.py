from typing import Dict, List
from ValidationTable import InforecastValidationTable
from DataColumn import DataColumn
import data_types
from helper_fundtions import generate_tag
from Table import Table
import os
import warnings
import shutil


class InforecastTracker:
    def __init__(self):
        self.data_table: Table = Table()
        self.change_table = Table()
        self.col_validation_table = InforecastValidationTable()

        # tag: DataColumn
        self.cols: Dict[str, DataColumn] = {}
        self.metadata: dict = {}
        self.name: str = None
        self.tag: str = None
        self.dir: str = None
        self.index: str = 'index'
        self.next_ind_val: int = 0

    def init(self, name: str, data_columns: [], metadata: dict, index: str = None):
        '''
        Function that initialises the tracker from scratch
        :param name: Name of the tracker
        :param data_columns: a list of DataColumn object that will be used to initialise the columns
        :param metadata: a dict with additional information; required: project_dir
        :param index: column to be used as index in the table, None to ignore
        :return: Nothing
        '''
        if not data_columns:
            warnings.warn('Please, specify data columns to initiate the Tracker')
            return False
        if 'project_dir' not in metadata.keys():
            warnings.warn('Project directory should be specified in the metadata: metadata[project_dir]')
            return False

        self.name = name
        self.tag = generate_tag(name)
        if index:
            self.index = index

        # Check cols and add to main list
        for col in data_columns:
            if type(col) != DataColumn:
                warnings.warn('Column type error. Columns need to be of type DataColumn')
                return False
            self.add_column(data_col=col)

        # Create the environment
        self.dir = os.path.join(metadata['project_dir'], self.tag)
        if os.path.isdir(self.dir):
            warnings.warn(f'Cannot initialise the tracker directory as a tracker with the same name exists already: '
                          f'{self.dir}')
            return False
        os.makedirs(self.dir)

        col_names = [x.get_tag() for x in data_columns] + [self.index]
        self.data_table.create_table(columns=col_names, index=self.index)

        # Create and save validation table, including drop-downs
        self.col_validation_table.init(data_cols=self.cols)

        # TODO: Create and save changes table

        return True

    def add_row(self, data: Dict[str, InforecastDataTypes]):
        '''
        Adds empty row to the table, then adds values to columns present in "data" param
        :param data: dictionary of type {col_tag: value}. Data can be specified for any number of cols, unspecified cols
                     will be assigned None
        :return true on success, false otherwise
        '''

        # Init raw with empty vals
        row = {}
        row[self.index] = self.next_ind_val
        self.next_ind_val += 1

        for col in self.cols:
            row[col] = None

        new_entry = False
        for item in data:
            if item in self.cols:
                val = data[item]
                if self.cols[item].validate(val):
                    row[item] = data[item]
                    new_entry = True
                else:
                    warnings.warn(f'Failed validation. Item: {data[item]} cannot be added to col with tag: {item}\n'
                                  f'(Name: {self.cols[item].get_name()}). Required type: {self.cols[item].get_type()}')

        if new_entry:
            self.data_table.insert_row(new_row=row)
            return True
        else:
            warnings.warn('There were no valid entries to add to the table')
            return False

    def add_rows(self, rows: List[Dict[str, InforecastDataTypes]]):
        '''
        Simplified version of adding multiple rows at the same time.
        Better to add rows one by one while handling potential errors
        :param rows: list of data to be added as rows
        :return: True only
        '''
        for row in rows:
            self.add_row(row)

        return True

    def amend_val(self, index_val: int, col_tag: str, value: InforecastDataTypes):
        '''
        Change an existing value given index and col
        :param index_val:
        :param col_tag:
        :param value:
        :return: true on success, false otherwise
        '''

        if col_tag not in self.cols.keys():
            warnings.warn(f'Provided tag not present in the table: {col_tag}')
            return False

        # validate the value to be inserted
        if not self.cols[col_tag].validate(value):
            warnings.warn(f'Validation failed. Provided value is not compatible with the column: {value}, type: {type(value)}'
                          f'\nRequired type: {self.cols[col_tag].get_type()}')
            return False

        self.data_table.set_value(indx=index_val, col=col_tag, val=value)

        return True

    def add_column(self, data_col: DataColumn):
        col_name = data_col.get_name()
        col_tag = data_col.get_tag()
        assert col_tag not in list(self.cols.keys()), f'Property with this tag already exists.\n' \
                                                      f'Tag: {col_tag}\nName: {col_name}'
        self.cols[col_tag] = data_col

    def save_data(self):
        self.data_table.save_table(table_path=self.dir, table_name=self.tag+'_data')

    def save_validation(self):
        self.col_validation_table.save_table(table_path=self.dir, table_name=self.tag+'_validation')

    def save_changes(self):
        # TODO
        pass

    def save(self):
        self.save_data()
        self.save_validation()
        self.save_changes()

    def get_cols_list(self):
        return list(self.cols.keys())


# Representative example
if __name__ == '__main__':
    from random import randint

    # Setup columns
    cols = []
    for i in range(5):
        dc_int = DataColumn(dtype=InforecastDataTypes.INT64, name=f'Test Number {i}')
        dc_int.set_limit({
            'min': InforecastDataTypes.to_int64(randint(0, 50)),
            'max': InforecastDataTypes.to_int64(randint(51, 1000))
        })

        dc_str = DataColumn(dtype=InforecastDataTypes.STR, name=f'Test String {i}')
        dc_str.set_limit({
            'max': InforecastDataTypes.to_int64(250)
        })

        cols.append(dc_int)
        cols.append(dc_str)

    dc_options = DataColumn(dtype=InforecastDataTypes.STR, name='Categories Col')
    options = [InforecastDataTypes.to_str('white'),
               InforecastDataTypes.to_str('red'),
               InforecastDataTypes.to_str('yellow'),
               InforecastDataTypes.to_str('blue')]
    if not dc_options.set_options(options):
        warnings.warn('Could not set options to Categories Col')
    cols.append(dc_options)

    # Prep the environment
    metadata = {'project_dir': 'test_dir/projects'}
    tracker_name = 'test tracker'
    tracker_tag = generate_tag(tracker_name)
    tracker_dir = os.path.join(metadata['project_dir'], tracker_tag)

    if os.path.isdir(tracker_dir):
        shutil.rmtree(tracker_dir)

    # Init tracker
    tracker = InforecastTracker()
    if not tracker.init(name=tracker_name, data_columns=cols, metadata=metadata, index=None):
        warnings.warn('Could not init tracker')

    print(f'Columns: {tracker.get_cols_list()}')

    # Add rows
    rows = [
            {
                'index': 0,
                'Test_Number_0': InforecastDataTypes.to_int64(randint(0, 10000)),
                'Test_Number_1': InforecastDataTypes.to_int64(randint(0, 10000)),
                'Test_Number_3': InforecastDataTypes.to_int64(randint(0, 10000)),
                'Test_String_4': InforecastDataTypes.to_str('here we go'),
                'Categories_Col': InforecastDataTypes.to_str('white')
            },
            {
                'index': 1,
                'Test_Number_2': InforecastDataTypes.to_int64(randint(0, 10000)),
                'Test_String_1': InforecastDataTypes.to_str('test string'),
                'Categories_Col': InforecastDataTypes.to_str('blue')
            },
            {
                'index': 2,
                'Test_Number_2': InforecastDataTypes.to_int64(randint(0, 10000)),
                'Test_String_1': InforecastDataTypes.to_str('test string'),
                'Categories_Col': InforecastDataTypes.to_str('yellow')
            }
            ]

    a = 10
    a = InforecastDataTypes.INT64.value(a)
    print(type(a))

    tracker.add_rows(rows)

    # Amend row value

    tracker.amend_val(index_val=1, col_tag='Test_Number_1', value=InforecastDataTypes.to_int64(randint(0, 10000)))
    tracker.amend_val(index_val=2, col_tag='Test_String_1', value=InforecastDataTypes.to_str('CHANGED'))

    # Save changes

    tracker.save()
