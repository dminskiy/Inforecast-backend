import warnings

from SdfKpi import SdfKpi
from KpiEnums import KpiTypes, KpiStatus, DevelopmentTypes, RibaStages


class SdfProject:
    def __init__(self, riba_stage: RibaStages, dev_type: DevelopmentTypes):
        self._current_riba_stage: RibaStages = riba_stage
        # only set once
        self._dev_type: DevelopmentTypes = dev_type
        self.kpis: dict = {}

    def set_riba_stage(self, new_riba_stage: RibaStages):
        self._current_riba_stage = new_riba_stage

        # TODO: trigger reevaluation of all KPIs

    def get_raw_score(self, kpi_identifier: str):
        if not self.verify_kpi_identifier(kpi_identifier):
            return None
        self.evaluate_kpi(kpi_identifier)

        return self.kpis[kpi_identifier].get_raw_score()

    def get_final_score(self, kpi_identifier: str):
        if not self.verify_kpi_identifier(kpi_identifier):
            return None
        self.evaluate_kpi(kpi_identifier)

        return self.kpis[kpi_identifier].get_final_score()

    def get_status(self, kpi_identifier: str):
        if not self.verify_kpi_identifier(kpi_identifier):
            return None
        self.evaluate_kpi(kpi_identifier)

        return self.kpis[kpi_identifier].get_status()

    def add_kpi(self, kpi_identifier: str, kpi_type: KpiTypes, input_args: dict, development_types: list,
                riba_stages: list, good_practice: float = None, leading_practice: float = None,
                upper_bound_norm: int = None, lower_bound_norm: int = None, reporting_only: bool = False):

        assert kpi_identifier not in self.kpis.keys(), f'Cannot add KPI as this KPI identifier ' \
                                                       f'already exists: {kpi_identifier}'

        kpi = SdfKpi(kpi_type=kpi_type,
                     input_args=input_args,
                     development_types=development_types,
                     riba_stages=riba_stages,
                     good_practice=good_practice,
                     leading_practice=leading_practice,
                     upper_bound_norm=upper_bound_norm,
                     lower_bound_norm=lower_bound_norm,
                     reporting_only=reporting_only)

        self.kpis[kpi_identifier] = kpi

    def kpi_isValid(self, kpi_identifier: str):
        if not self.kpis[kpi_identifier].validate_riba_stage(self._current_riba_stage):
            return False
        if not self.kpis[kpi_identifier].validate_dev_type(self._dev_type):
            return False

        return True

    def evaluate_kpi(self, kpi_identifier: str):
        if not self.verify_kpi_identifier(kpi_identifier):
            return False
        if not self.kpi_isValid(kpi_identifier):
            return False

        if not self.kpis[kpi_identifier].ready():
            self.kpis[kpi_identifier].evaluate()

        return True

    def verify_kpi_identifier(self, kpi_identifier: str):
        return kpi_identifier in self.kpis.keys(), f'KPI identified is not in the list of KPIs: {kpi_identifier}'

    def print_summary(self, kpi_identifier: str, in_val: dict = None, kpi_type: KpiTypes = None):
        in_val = in_val if in_val else 'Unknown'
        kpi_type = kpi_type if kpi_type else 'Unknown'
        print(f'\nKPI Summary:'
              f'\nKPI Identifier: {kpi_identifier}'
              f'\nKPI type:       {kpi_type}'
              f'\nInput val:      {in_val}'
              f'\nRaw score:      {self.get_raw_score(kpi_identifier)}'
              f'\nFinal score:    {self.get_final_score(kpi_identifier)}'
              f'\nFinal status:   {self.get_status(kpi_identifier)}')


# TODO: Test normalisation
# TODO: Add RIBA stages and Dev Types
# TODO: Add KPI name

if __name__ == '__main__':
    TEST_KPI_NUMBER = False
    TEST_KPI_NUMBERS_SET = False
    TEST_QUIZ = True
    TEST_CHECKBOXES = False
    TEST_BINARY = False

    project = SdfProject(riba_stage=RibaStages.FIVE, dev_type=DevelopmentTypes.COMMERCIAL)
    kpis2test = []

    if TEST_KPI_NUMBER:
        new_kpi = {
            'identifier': 'VP1',
            'riba_stages': [RibaStages.ONE, RibaStages.TWO, RibaStages.THREE, RibaStages.FOUR, RibaStages.FIVE,
                            RibaStages.SIX, RibaStages.SEVEN],
            'dev_types': [DevelopmentTypes.COMMERCIAL, DevelopmentTypes.RESIDENTIAL, DevelopmentTypes.MASTERPLAN],
            'type': KpiTypes.NUMBER,
            'input': {
                'val': 76
            },
            'gp': 65,
            'lp': 85,
            'upper_bound': 100,
            'lower_bound': 0,
            'reporting_only': False
        }

        kpis2test.append(new_kpi)

    if TEST_KPI_NUMBERS_SET:
        def hw1_calculation(vehicles: dict):
            assert 'cars' in vehicles
            assert 'vans' in vehicles
            assert 'lorries' in vehicles

            return vehicles['cars'] * 50 + vehicles['vans'] * 100 + vehicles['lorries'] * 150

        new_kpi = {
            'identifier': 'HW1',
            'riba_stages': [RibaStages.ZERO, RibaStages.TWO, RibaStages.FIVE, RibaStages.SEVEN],
            'dev_types': [DevelopmentTypes.COMMERCIAL, DevelopmentTypes.MASTERPLAN],
            'type': KpiTypes.NUMBERS_SET,
            'input': {
                'vals': {'cars': 100,
                         'vans': 20,
                         'lorries': 5
                         },
                'func': hw1_calculation
            },
            'gp': 8000,
            'lp': 10000,
            'upper_bound': 10000,
            'lower_bound': 0,
            'reporting_only': False
        }

        kpis2test.append(new_kpi)

    if TEST_QUIZ:
        pass

    if TEST_CHECKBOXES:
        pass

    if TEST_BINARY:
        pass

    for _kpi in kpis2test:
        project.add_kpi(kpi_identifier=_kpi['identifier'],
                        kpi_type=_kpi['type'],
                        input_args=_kpi['input'],
                        good_practice=_kpi['gp'],
                        leading_practice=_kpi['lp'],
                        upper_bound_norm=_kpi['upper_bound'],
                        lower_bound_norm=_kpi['lower_bound'],
                        reporting_only=_kpi['reporting_only'],
                        development_types=_kpi['dev_types'],
                        riba_stages=_kpi['riba_stages'])

        assert project.verify_kpi_identifier(_kpi['identifier']), 'KPI verification error'

        project.evaluate_kpi(kpi_identifier=_kpi['identifier'])
        project.print_summary(kpi_identifier=_kpi['identifier'], kpi_type=_kpi['type'], in_val=_kpi['input'])
