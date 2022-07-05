
class KPI_INPUT:
    def __init__(self):
        self.input_types = {'number', 'quiz', 'checkboxes', 'reporting_only', 'binary'}
        self.type = None


class KPI:
    def __init__(self):
        self.name = None
        self.dev_type = None
        self.riba_stages = None
        self.input: KPI_INPUT = None
