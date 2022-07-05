import warnings

from typing import List

from helper_fundtions import generate_tag
from data_types import InforecastDataTypes


class DataColumn:
    def __init__(self, dtype: InforecastDataTypes, name: str):
        '''
        :param dtype: type of the data stored in the column
        :param name: name as displayed in the column
        '''

        self.dtype: InforecastDataTypes = dtype
        self.name: str = name
        self.tag: str = generate_tag(self.name)  # to be used as a handler in a table
        # (min, max) -> for numbers; int(max) -> for str
        self.limit: () = None
        self.options: List[dtype] = []
        self.num_options: int = 0

        # default limit for strings, #chars
        if dtype == InforecastDataTypes.STR:
            self.limit = (0, 50)

    def print(self):
        print(f'Column Name   : {self.name}\n'
              f'Column Tag    : {self.tag}\n'
              f'Column Type   : {self.dtype}\n'
              f'Column limit  : {self.limit}\n'
              f'Column options: {self.options}')

    def get_name(self):
        return self.name

    def get_tag(self):
        return self.tag

    def get_type(self):
        return self.dtype

    def get_limit(self):
        return self.limit

    def get_options(self):
        return self.options

    def type_isValid(self, value):
        return InforecastDataTypes(type(value)) == self.dtype

    def limit_isValid(self, value):
        if not self.limit:
            return True

        if self.dtype == InforecastDataTypes.STR:
            value = len(value)

        return self.limit[1] > value > self.limit[0]

    def option_isValid(self, value):
        if not self.options:
            return True
        return value in self.options

    def validate(self, value):
        if not self.type_isValid(value):
            return False
        if not self.limit_isValid(value):
            return False
        if not self.option_isValid(value):
            return False

        return True

    def set_options(self, options: []):
        if not options:
            warnings.warn("Setting column options to an empty list")
            self.options = []
            return True

        for val in options:
            if not self.validate(val):
                warnings.warn(f"Cannot set options for the column as invalid:\n"
                              f"Value: {val}, Type: {type(val)};"
                              f"\nSupported type: {self.dtype}; Current limit: {self.limit}")
                return False

        self.options = options
        self.num_options = len(self.options)
        return True

    def set_limit(self, limit_dict: dict):
        if self.dtype in NUM_TYPES:
            assert list(limit_dict.keys()).sort() == ['min', 'max'].sort(), "For data types containing numbers, the " \
                                                                            "limit_dict must only contain 'min' " \
                                                                            "and 'max' as key"
            for key in limit_dict.keys():
                assert InforecastDataTypes(type(limit_dict[key])) == self.dtype, f"limit_dict key type must be the " \
                                                                                f"same as the original " \
                                                                                f"dtype: {self.dtype}"
            self.limit = (limit_dict['min'], limit_dict['max'])

        elif self.dtype == InforecastDataTypes.STR:
            assert list(limit_dict.keys()) == ['max'], "For strings, the limit_dict should only have 'max' " \
                                                       "as the key"
            assert InforecastDataTypes(type(limit_dict['max'])) == InforecastDataTypes.INT64, "For strings the " \
                                                                                            "limit_dict['max'] " \
                                                                                            "should be of type INT64"
            self.limit = (0, limit_dict['max'])

        else:
            warnings.warn('At this stage, limits can only be set for numbers and strings')
            self.limit = None


if __name__ == '__main__':
    a = DataColumn(dtype=InforecastDataTypes.INT64, name='Test Number')
    limit = {
         'min': InforecastDataTypes.to_int64(10),
         'max': InforecastDataTypes.to_int64(100)
    }
    a.set_limit(limit_dict=limit)
    a.print()
    print()

    b = DataColumn(dtype=InforecastDataTypes.STR, name='Test String')
    limit = {
        'max': InforecastDataTypes.to_int64(250)
    }
    b.set_limit(limit_dict=limit)
    b.print()
