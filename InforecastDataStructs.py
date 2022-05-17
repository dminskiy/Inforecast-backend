import enum
import warnings
import numpy as np


class SupportedDataTypes(enum.Enum):
    STR = np.str_
    DOUBLE = np.double
    BOOL = np.bool_

    UINT8 = np.uint8
    INT16 = np.int16
    INT32 = np.int32
    INT64 = np.int64
    FLOAT32 = np.float32
    FLOAT64 = np.float64


class DataColumn:
    def __init__(self, dtype: SupportedDataTypes, name: str):
        '''
        :param dtype: type of the data stored in the column
        :param name: name as displayed in the column
        '''

        self.dtype = dtype
        self.name = name
        self.tag = self._generate_tag()  # to be used as a handler in a table
        self.limit = None

    def _generate_tag(self):
        # Replace forbidden chars in the name to store in the table
        tag = self.name.replace(' ', '_')
        return tag

    def print(self):
        print(f'Column Name : {self.name}\n'
              f'Column Tag  : {self.tag}\n'
              f'Column Type : {self.dtype}\n'
              f'Column limit: {self.limit}')

    def get_name(self):
        return self.name

    def get_tag(self):
        return self.tag

    def get_type(self):
        return self.dtype

    def set_limit(self, limit_dict: dict):
        if self.dtype in [SupportedDataTypes.UINT8,
                          SupportedDataTypes.INT16,
                          SupportedDataTypes.INT32,
                          SupportedDataTypes.INT64,
                          SupportedDataTypes.FLOAT32,
                          SupportedDataTypes.FLOAT64,
                          SupportedDataTypes.DOUBLE]:

            assert list(limit_dict.keys()).sort() == ['min', 'max'].sort(), "For data types containing numbers, the " \
                                                                            "limit_dict must only contain 'min' " \
                                                                            "and 'max' as key"
            for key in limit_dict.keys():
                assert SupportedDataTypes(type(limit_dict[key])) == self.dtype, f"limit_dict key type must be the " \
                                                                                f"same as the original " \
                                                                                f"dtype: {self.dtype}"
            self.limit = (limit_dict['min'], limit_dict['max'])

        elif self.dtype == SupportedDataTypes.STR:
            assert list(limit_dict.keys()) == ['max'], "For strings, the limit_dict should only have 'max' " \
                                                       "as the key"
            assert SupportedDataTypes(type(limit_dict['max'])) == SupportedDataTypes.INT64, "For strings the " \
                                                                                            "limit_dict['max'] " \
                                                                                            "should be of type INT64"
            self.limit = limit_dict['max']

        else:
            warnings.warn('At this stage, limits can only be set for numbers and strings')
            self.limit = None


if __name__ == '__main__':
    def to_int64(val):
        return SupportedDataTypes.INT64.value(val)

    a = DataColumn(dtype=SupportedDataTypes.INT64, name='Test Number')
    limit = {
         'min': to_int64(10),
         'max': to_int64(100)
    }
    a.set_limit(limit_dict=limit)
    a.print()
    print()

    b = DataColumn(dtype=SupportedDataTypes.STR, name='Test String')
    limit = {
        'max': to_int64(250)
    }
    b.set_limit(limit_dict=limit)
    b.print()
