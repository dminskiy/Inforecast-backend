import enum


class KpiTypes(enum.Enum):
    UNDEFINED = enum.auto()
    NUMBER = enum.auto()
    NUMBERS_SET = enum.auto()
    QUIZ = enum.auto()
    CHECKBOXES = enum.auto()
    BINARY = enum.auto()


class KpiStatus(enum.Enum):
    UNDEFINED = enum.auto()
    NEEDS_IMPROVEMENT = enum.auto()
    GOOD_PRACTICE = enum.auto()
    LEADING_PRACTICE = enum.auto()
    REPORTING_ONLY = enum.auto()
    NOT_APPLICABLE = enum.auto()


class RibaStages(enum.Enum):
    ZERO = enum.auto()
    ONE = enum.auto()
    TWO = enum.auto()
    THREE = enum.auto()
    FOUR = enum.auto()
    FIVE = enum.auto()
    SIX = enum.auto()
    SEVEN = enum.auto()


class DevelopmentTypes(enum.Enum):
    RESIDENTIAL = enum.auto()
    COMMERCIAL = enum.auto()
    MASTERPLAN = enum.auto()