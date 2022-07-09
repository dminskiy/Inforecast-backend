import enum
from abc import ABC


class KpiTypes(enum.Enum):
    UNDEFINED = enum.auto()
    NUMBER = enum.auto()
    NUMBERS_SET = enum.auto()
    QUIZ = enum.auto()
    CHECKBOXES = enum.auto()
    BINARY = enum.auto()


class KpiStatus(enum.Enum):
    UNDEFINED = enum.auto()
    GOOD_PRACTICE = enum.auto()
    LEADING_PRACTICE = enum.auto()
    REPORTING_ONLY_PRACTICE = enum.auto()


class RibaStages(enum.Enum):
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


class KpiBase(ABC):
    def set_evaluation_range(self, lower_bound: int, upper_bound: int):
        ''' Min and max after raw evaluation, to be used in normalisation to shift the limits '''
        pass

    def set_status_range(self, good_practice: float, leading_practice: float):
        ''' Set ranges for KPI status in terms of final range (0-100) '''
        pass

    def get_raw_score(self):
        ''' KPI Score in the original bounds '''
        pass

    def get_final_score(self):
        ''' KPI score between 0 and 100 '''
        pass

    def get_status(self):
        ''' KPI status: Good/Leading Practice, Not Available, Reporting Only '''
        pass

    def evaluate(self):
        ''' Calculates raw and final scores, defines status '''
        pass

    def normalise(self):
        ''' Normalise the value range to a standard 0-100 '''
        pass


class SdfKpiInput:
    def __init__(self, kpi_type: KpiTypes, input_args: dict):
        self._type: KpiTypes = kpi_type
        self._input_args: dict = input_args

        if self._type == KpiTypes.NUMBER:
            ''' val is used directly '''
            assert 'val' in self._input_args

        elif self._type == KpiTypes.NUMBERS_SET:
            ''' 
                vals are used in func to calculate the score.
                func only set in code
            '''
            assert 'vals' in self._input_args
            assert 'func' in self._input_args

        elif self._type == KpiTypes.QUIZ or KpiTypes.CHECKBOXES or KpiTypes.BINARY:
            'questions = {question: {reply 1: score1; reply 2: score2}}'
            assert 'questions' in self._input_args

            if self._type == KpiTypes.CHECKBOXES or KpiTypes.BINARY:
                if self._type == KpiTypes.BINARY:
                    # Only one question is expected
                    assert list(self._input_args['questions'].keys()) == 1

                # Only two reply options: yes, no
                for question in list(self._input_args['questions'].keys()):
                    # expected 'positive': bool
                    assert len(list(self._input_args['questions'][question])) == 1


class SdfKpi(KpiBase, SdfKpiInput):
    def __init__(self, kpi_type: KpiTypes, input_args: dict):
        super(SdfKpi, self).__init__(kpi_type, input_args)

        self._riba_stages: list = []
        self._development_types: list = []

        self._upper_bound: int = None
        self._lower_bound: int = None

        self._good_practice_thr: float = None
        self._leading_practice_thr: float = None

        self._raw_score: float = None
        self._final_score: int = None
        self._final_status: KpiStatus = KpiStatus.UNDEFINED

    def set_evaluation_range(self, lower_bound: int, upper_bound: int):
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound

    def set_status_range(self, good_practice: float, leading_practice: float):
        self._good_practice_thr = good_practice
        self._leading_practice_thr = leading_practice

    def get_raw_score(self):
        return self._raw_score

    def get_final_score(self):
        return self._final_score

    def get_status(self):
        return self._final_status

    def normalise(self):
        if self._type in [KpiTypes.NUMBER, KpiTypes.NUMBERS_SET]:
            if self._raw_score < self._good_practice_thr:
                self._final_score = int(self._raw_score * 50./self._good_practice_thr + 0.5)
            elif self._good_practice_thr < self._raw_score <= self._leading_practice_thr:
                self._final_score = int(50. + 50.*((self._leading_practice_thr - self._raw_score)/(self._leading_practice_thr-self._good_practice_thr)) + 0.5)
            else:
                self._final_score = 100
        else:
            raise NotImplementedError('Linear normalisation yet to be implemented')

    def evaluate(self):
        if self._type == KpiTypes.NUMBER:
            self.evaluate_number()
        elif self._type == KpiTypes.NUMBERS_SET:
            self.evaluate_numbers_set()
        elif self._type == KpiTypes.QUIZ:
            self.evaluate_quiz()
        elif self._type == KpiTypes.CHECKBOXES:
            self.evaluate_checkboxes()
        elif self._type == KpiTypes.BINARY:
            self.evaluate_binary()
        else:
            raise RuntimeError('Cannot Evaluate KPI. KPI type is not defined')

    def evaluate_number(self):
        pass

    def evaluate_numbers_set(self):
        pass

    def evaluate_quiz(self):
        pass

    def evaluate_checkboxes(self):
        pass

    def evaluate_binary(self):
        pass


class SdfProject:
    def __init__(self):
        self.kpis: dict = {}

    def add_kpi(self, kpi_identifier: str, kpi_type: KpiTypes, input_args: dict):
        assert kpi_identifier not in self.kpis.keys(), f'Cannot add KPI as this KPI identifier ' \
                                                       f'already exists: {kpi_identifier}'
        kpi = SdfKpi(kpi_type=kpi_type, input_args=input_args)
        self.kpis[kpi_identifier] = kpi
