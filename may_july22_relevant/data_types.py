import datetime

import numpy as np
from abc import ABC


class InData(ABC):
    def __eq__(self, other):
        ...

    def type(self):
        ''' Returns the raw type of the data '''
        ...

    def raw(self):
        ''' Return the raw value of the data '''
        ...


class InNumber(InData):
    def __init__(self, value=None):
        self._value = np.double(value)

    def type(self):
        return type(self.raw())

    def raw(self):
        return self._value

    # Operations (total: 7)

    def __add__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value + other.raw())

        raise RuntimeError('Datatypes do not match')

    def __sub__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value - other.raw())

        raise RuntimeError('Datatypes do not match')

    def __mul__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value * other.raw())

        raise RuntimeError('Datatypes do not match')

    def __pow__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value ** other.raw())

        raise RuntimeError('Datatypes do not match')

    def __truediv__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value / other.raw())

        raise RuntimeError('Datatypes do not match')

    def __floordiv__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value // other.raw())

        raise RuntimeError('Datatypes do not match')

    def __mod__(self, other):
        if isinstance(other, InNumber):
            return InNumber(self._value % other.raw())

        raise RuntimeError('Datatypes do not match')

    # Comparisons (total: 6)

    def __eq__(self, other):
        if isinstance(other, InNumber):
            return self._value == other.raw()
        return False

    def __ne__(self, other):
        if isinstance(other, InNumber):
            return self._value != other.raw()
        return False

    def __lt__(self, other):
        if isinstance(other, InNumber):
            return self._value < other.raw()
        return False

    def __le__(self, other):
        if isinstance(other, InNumber):
            return self._value <= other.raw()
        return False

    def __gt__(self, other):
        if isinstance(other, InNumber):
            return self._value > other.raw()
        return False

    def __ge__(self, other):
        if isinstance(other, InNumber):
            return self._value >= other.raw()
        return False


class InDateDelta(InData):
    def __init__(self, days=0, weeks=0, hours=0, minutes=0, _timedelta: datetime.timedelta = None):
        self._value = datetime.timedelta(days=days, weeks=weeks, hours=hours, minutes=minutes)
        if _timedelta:
            self._value = _timedelta

    def raw(self):
        return self._value

    def type(self):
        return type(self._value)

    def __eq__(self, other):
        if isinstance(other, InDateDelta):
            return self._value == other.raw()
        return False

    def __str__(self):
        return self.raw().__str__()


class InDate(InData):
    def __init__(self, year=1, month=1, day=1, hour=1, minute=1, _datetime: datetime.datetime = None):
        self._value = datetime.datetime(year, month, day, hour, minute)
        if _datetime:
            self._value = _datetime

    def __eq__(self, other):
        if isinstance(other, InDate):
            return self._value == other.raw()
        return False

    def type(self):
        return type(self.raw())

    def raw(self):
        return self._value

    def now(self):
        self._value = datetime.datetime.now()
        return self.raw()

    def __str__(self):
        return self.raw().__str__()

    def year(self):
        return self._value.year

    def month(self):
        return self._value.month

    def day(self):
        return self._value.day

    def hour(self):
        return self._value.hour

    def minute(self):
        return self._value.minute

    # Operations (total: 7)

    def __add__(self, other):
        '''
        Addition between InData and InDataDelta
        :param other: InDataDelta object
        :return: InDate
        '''
        if isinstance(other, InDateDelta):
            dt = self._value + other.raw()
            return InDate(_datetime=dt)
        raise RuntimeError('For addition use: InData & InDateDelta')

    def __sub__(self, other):
        '''
        Two options for subtraction: InDate - InDate -> InDateDelta or InDate - InDateDelta -> InDate
        :param other: either (1): InDate (2): InDateDelta
        :return: either (1): InDateDelta (2) InDate
        '''
        if isinstance(other, InDate):
            delta = self._value - other.raw()
            return InDateDelta(_timedelta=delta)
        elif isinstance(other, InDateDelta):
            dt = self._value - other.raw()
            return InDate(_datetime=dt)
        else:
            raise RuntimeError('Two options for subtraction:'
                               '\nInDate - InDate -> InDateDelta or InDate - InDateDelta -> InDate')


class InText(InData):
    def __init__(self, value):
        self._value = str(value)

    def __eq__(self, other):
        if isinstance(other, InText):
            return self._value == other.raw()
        return False

    def type(self):
        return type(self.raw())

    def raw(self):
        return self._value

    def __add__(self, other):
        if isinstance(other, InText):
            return InText(self._value + other.raw())

        raise RuntimeError('Datatypes do not match')

    def len(self):
        return len(self.raw())


if __name__ == "__main__":
    from random import random, randint
    check_InNumber = True
    check_InDate = True
    check_InText = True

    # Check InNumber
    if check_InNumber:
        a = randint(0, 10) + random()
        b = randint(0, 10) + random()

        a_in = InNumber(a)
        b_in = InNumber(b)

        a_std = a_in.type()(a)
        b_std = b_in.type()(b)

        # Operations
        assert (a_in + b_in).raw() == (a_std + b_std), print(f'(a_in + b_in): {(a_in + b_in).raw()}; '
                                                             f'(a_std + b_std): {(a_std + b_std)}')
        assert (a_in - b_in).raw() == (a_std - b_std), print(f'(a_in - b_in): {(a_in - b_in).raw()}; '
                                                             f'(a_std - b_std): {(a_std - b_std)}')
        assert (a_in * b_in).raw() == (a_std * b_std), print(f'(a_in * b_in): {(a_in * b_in).raw()};'
                                                             f' (a_std * b_std): {(a_std * b_std)}')
        assert (a_in ** b_in).raw() == (a_std ** b_std), print(f'(a_in ** b_in): {(a_in ** b_in).raw()};'
                                                               f' (a_std ** b_std): {(a_std ** b_std)}')
        assert (a_in / b_in).raw() == (a_std / b_std), print(f'(a_in / b_in): {(a_in / b_in).raw()};'
                                                             f' (a_std / b_std): {(a_std / b_std)}')
        assert (a_in // b_in).raw() == (a_std // b_std), print(f'(a_in // b_in): {(a_in // b_in).raw()};'
                                                               f' (a_std // b_std): {(a_std // b_std)}')
        assert (a_in % b_in).raw() == (a_std % b_std), print(f'(a_in % b_in): {(a_in % b_in).raw()};'
                                                             f' (a_std % b_std): {(a_std % b_std)}')

        # Comparisons
        assert (a_in == b_in) == (a_std == b_std)
        assert (a_in != b_in) == (a_std != b_std)
        assert (a_in < b_in) == (a_std < b_std)
        assert (a_in <= b_in) == (a_std <= b_std)
        assert (a_in > b_in) == (a_std > b_std)
        assert (a_in >= b_in) == (a_std >= b_std)

        print('InNumbers are good')

    # Check date management
    if check_InDate:
        a = InDate(year=2005, day=23, month=3, minute=14, hour=23)
        b = InDateDelta(days=452, hours=321)
        c = a + b

        assert (c-a).__str__() == b.__str__(), print(f'(c-a): {(c-a).__str__()}; '
                                                     f'b: {b.__str__()}')
        assert (c-b).__str__() == a.__str__(), print(f'(c-b): {(c-b).__str__()}; '
                                                     f'a: {a.__str__()}')

        print('InDates are good')

    if check_InText:

        one = 'In'
        two = 'Text'

        a = InText(one)
        b = InText(two)

        assert (a+b).raw() == one+two, print(f'(a+b).raw() {(a+b).raw()}; one+two: {one+two}')

        print('InText is good')

    print('All Good')
