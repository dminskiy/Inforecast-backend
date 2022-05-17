import numpy as np
import datetime

import pandas as pd

from DataStructsHandler import DataCell
from DatabaseHandler import Table


class PropertiesPackage:
    def __init__(self):
        self._properties = {}

    def add_property(self, ppty: DataCell):
        assert ppty.col() not in self._properties.keys(), f'Property with this name already exists: {ppty.col()}'
        self._properties[ppty.col()](ppty)

    def set_property(self, ppty_name, val):
        assert ppty_name in self._properties.keys(), f'Selected property not in the list: {ppty_name}'
        self._properties[ppty_name].set_val(val)

    def to_list(self):
        return [self._properties[key].col() for key in self._properties.keys()]

    def to_dict(self):
        out_dict = {}
        for key in self._properties.keys():
            out_dict[key] = self._properties[key].get_val()

        return out_dict


class WorkPackageProperties(PropertiesPackage):
    def __init__(self):
        super(PropertiesPackage, self).__init__()
        # WP Compulsory Properties
        self._properties = {
            'WPId': DataCell(col='WPId', dtype=np.str, is_cumulative=False),
            'WPName': DataCell(col='WPName', dtype=np.str, is_cumulative=False),
            'cost_baseline': DataCell(col='cost_baseline', dtype=np.float, is_cumulative=True),
            'cost_forecast': DataCell(col='cost_forecast', dtype=np.float, is_cumulative=True),
            'start_date_baseline': DataCell(col='start_date_baseline', dtype=datetime.datetime, is_cumulative=True),
            'end_date_baseline': DataCell(col='end_date_baseline', dtype=datetime.datetime, is_cumulative=True),
            'start_date_forecast': DataCell(col='start_date_forecast', dtype=datetime.datetime, is_cumulative=True),
            'end_date_forecast': DataCell(col='end_date_forecast', dtype=datetime.datetime, is_cumulative=True),
            'completion_status': DataCell(col='completion_status', dtype=np.bool, is_cumulative=True),
            'responsible_person': DataCell(col='responsible_person', dtype=np.str, is_cumulative=True),
        }


class WPFamilyProperties(PropertiesPackage):
    def __init__(self):
        super(PropertiesPackage, self).__init__()
        # WP Compulsory Properties
        self._properties = {
            'WPId': DataCell(col='WPId', dtype=np.str, is_cumulative=False),
            'level': DataCell(col='WPName', dtype=np.str, is_cumulative=False),
            'child': DataCell(col='cost_baseline', dtype=np.str, is_cumulative=False),
            'parent': DataCell(col='cost_forecast', dtype=np.str, is_cumulative=False)
        }


class WorkPackage(WorkPackageProperties):
    def __init__(self, ):
        super(WorkPackage, self).__init__()
        # WP Properties Auto-defined
        self._id = None
        self._lvl = None
        self._children = []
        self._parent = None

    def list_properties(self):
        return self.to_list()

    def create(self, name: str, level: int, count: int, family_table: Table(), parent: str = None):
        # WP Properties Auto-defined
        self._lvl = level
        self._children = []
        self._parent = parent

        self._id = self.generate_id(count)

        self._properties['WPId'].set_val(self._id)
        self._properties['WPName'].set_val(name)

        self.update_family_table()

    def load(self, wp_id: str, properties_table: Table, relationships_table: Table):
        assert properties_table.columns().sort() == self.list_properties().sort(), \
            f'Property table incompatible with the Work Package'

        # load properties
        for ppty_name in self._properties.keys():
            val = properties_table.get_value_from_index(indx=wp_id, col=ppty_name)
            if type(val) == pd.Timestamp:
                val = val.to_pydatetime()

            required_type = self._properties[ppty_name].type()
            if type(val) != required_type:
                val = required_type(val)

            self._properties[ppty_name].set_val(val)

        self._properties['WPId'].set_val(wp_id)
        self._id = wp_id

        # set relationships


    def get_ppty_value(self, ppty_name: str):
        assert ppty_name in self._properties.keys(), f'Property is not present in the Work Package'

    def generate_id(self, count):
        return f'{self._lvl}.{count}.{self._parent}' if self._parent else f'{self._lvl}.{count}'

    def update_family_table(self, children: list, parent: str, family_table: Table()):
        fam_properties = WPFamilyProperties()

        fam_properties.set_property('parent', parent)
        fam_properties.set_property('level', self._lvl)
        fam_properties.set_property('WPId', self._id)

        row = fam_properties.to_dict()

        #TODO
        # if not children add row

        for child in children:
            # add row per child
            pass

    def print(self):

        print('\nWork Package INFO:')

        for ppty_name in self._properties.keys():
            print(f'{self._properties[ppty_name].col()}: {self._properties[ppty_name].get_val()}')

        print(f'\nLevel: {self._lvl}')
        print(f'Parent: {self._parent}')
        print(f'Children: {self._children}')
