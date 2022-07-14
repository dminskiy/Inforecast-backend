from abc import ABC
from KpiEnums import KpiTypes, KpiStatus, DevelopmentTypes, RibaStages


class KpiBase(ABC):
    def set_evaluation_range(self, lower_bound: int, upper_bound: int):
        ''' Min and max after raw evaluation, to be used in normalisation to shift the limits '''
        pass

    def set_practice_thr(self, good_practice: float, leading_practice: float):
        ''' Set good and leading practice thresholds in terms of raw range. Used to define status '''
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

    def normalise(self, val: float):
        ''' Normalise the value range to a standard 0-100 '''
        pass

    def set_riba_stages(self, riga_stages: list):
        ''' Set riba_stages to which this KPI applies '''
        pass

    def set_dev_types(self, dev_types: list):
        ''' Set development type to which this KPI applies '''
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
            '''questions = 
                            {Question String: 
                                                {
                                                    reply_option1: score1; 
                                                    reply_option2: score2; 
                                                    reply: <option 1 or 2>
                                                }
                            }
            '''
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
    def __init__(self, kpi_type: KpiTypes, input_args: dict, development_types: list, riba_stages: list,
                 good_practice: float = None, leading_practice: float = None,
                 upper_bound_norm: int = None, lower_bound_norm: int = None, reporting_only: bool = False):
        super(SdfKpi, self).__init__(kpi_type, input_args)

        self._riba_stages: list = self.add_riba_stages(riba_stages)
        self._development_types: list = self.add_dev_types(development_types)

        self._upper_bound: int = upper_bound_norm
        self._lower_bound: int = lower_bound_norm

        # Given in terms of raw score
        self._good_practice_thr: float = good_practice
        self._leading_practice_thr: float = leading_practice
        self._reporting_only: bool = reporting_only

        self._raw_score: float = None
        self._final_score: int = None
        self._final_status: KpiStatus = KpiStatus.UNDEFINED

    def ready(self):
        if self._final_score:
            return True
        else:
            return False

    def validate_riba_stage(self, project_riba_stage: RibaStages):
        return project_riba_stage in self._riba_stages

    def validate_dev_type(self, project_dev_type: DevelopmentTypes):
        return project_dev_type in self._development_types

    def set_evaluation_range(self, lower_bound: int, upper_bound: int):
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound

    def set_practice_thr(self, good_practice: float, leading_practice: float):
        self._good_practice_thr = good_practice
        self._leading_practice_thr = leading_practice

    def get_raw_score(self):
        return self._raw_score

    def get_final_score(self):
        return self._final_score

    def get_status(self):
        return self._final_status

    def add_dev_types(self, dev_types: list):
        assert dev_types, f'Empty development types'
        out = []
        for dev_type in dev_types:
            assert type(dev_type) == DevelopmentTypes
            out.append(dev_type)

        return out

    def add_riba_stages(self, riba_stages: list):
        assert riba_stages, f'Empty development types'
        out = []
        for riba_stage in riba_stages:
            assert type(riba_stage) == RibaStages
            out.append(riba_stage)

        return out

    def normalise(self, val: float):
        if self._type in [KpiTypes.NUMBER, KpiTypes.NUMBERS_SET]:
            if val < self._good_practice_thr:
                norm = int(val * 50./self._good_practice_thr + 0.5)
            elif self._good_practice_thr < val <= self._leading_practice_thr:
                norm = int(50. + 50.*((self._leading_practice_thr - val)/(self._leading_practice_thr - self._good_practice_thr)) + 0.5)
            else:
                norm = 100
        else:
            norm = None
            raise NotImplementedError('Linear normalisation yet to be implemented')

        return norm

    def evaluate(self):
        # Evaluate the raw score, final score and status
        if self._type == KpiTypes.NUMBER:
            self.evaluate_number()
        elif self._type == KpiTypes.NUMBERS_SET:
            self.evaluate_numbers_set()
        elif self._type == KpiTypes.QUIZ:
            self.evaluate_questions()
        elif self._type == KpiTypes.CHECKBOXES:
            self.evaluate_questions()
        elif self._type == KpiTypes.BINARY:
            self.evaluate_questions()
        else:
            raise RuntimeError('Cannot evaluate KPI. KPI type is not defined')

        self.calculate_status()
        return True

    def calculate_status(self):
        assert self._raw_score, 'Raw score is required to define the KPI Status'

        if self._reporting_only:
            self._final_status = KpiStatus.REPORTING_ONLY
            return

        if not self._good_practice_thr and not self._leading_practice_thr:
            self._final_status = KpiStatus.UNDEFINED
            return

        if self._good_practice_thr < self._raw_score < self._leading_practice_thr:
            self._final_status = KpiStatus.GOOD_PRACTICE
        elif self._raw_score >= self._leading_practice_thr:
            self._final_status = KpiStatus.LEADING_PRACTICE
        elif self._raw_score < self._good_practice_thr:
            self._final_status = KpiStatus.NEEDS_IMPROVEMENT
        else:
            raise RuntimeError('Status evaluation error: out of bounds')

    def evaluate_number(self):
        assert 'val' in self._input_args.keys(), 'Key [val] needs to be in the input arguments'

        self._raw_score = self._input_args['val']
        self._final_score = self.normalise(self._raw_score)

    def evaluate_numbers_set(self):
        assert 'vals' in self._input_args.keys(), 'Key [vals] needs to be in the input arguments'
        assert 'func' in self._input_args.keys(), 'Key [func] needs to be in the input arguments'

        vals = self._input_args['vals']
        function = self._input_args['func']

        self._raw_score = function(vals)
        self._final_score = self.normalise(self._raw_score)

    def evaluate_questions(self):
        assert 'questions' in self._input_args.keys(), 'Key [questions] needs to be in the input arguments'

        questions = self._input_args['questions']

        cum_score = 0
        for question in questions:
            '''
                'Question String' = {
                                    'reply_option1': score1,
                                    'reply_option2': score2,
                                    'reply': <reply_option1 or 2>
                                }
            '''
            assert 'reply' in questions[question], 'Reply is not available for the question'

            reply = questions[question]['reply']

            assert reply, 'Reply for the question was not selected'
            assert reply in questions[question], f'Reply is not available in the list of selectable options'

            cum_score += questions[question][reply]

        self._raw_score = cum_score
        self._final_score = self.normalise(self._raw_score)
