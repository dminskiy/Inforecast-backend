import pandas as pd


class ProjectSetupParams:
    def __init__(self):
        self.name = None
        self.id = None

        self.wp_table_details = {
        }


class Project:
    def __init__(self, setup_params: ProjectSetupParams):
        # Project Properties
        self.name = setup_params.name
        self.id = setup_params.id

        # Project Setup Parameters
        self.setup_parameters = setup_params

        # Project Elements
        self.work_packages = WorkPackageTable(self.setup_parameters.wp_table_details)


class WorkPackage:
    def __init__(self, wp_id=None):
        # WP Properties Auto-defined
        self.id = wp_id
        self.lvl = None
        self.children = []
        self.parent = None

        # WP Compulsory Properties
        self.compulsory_ppts = {
            {
                'cumulative':
                    {
                        'cost_baseline': None,
                        'cost_forecast': None,
                        'start_date_baseline': None,
                        'end_date_baseline': None,
                        'start_date_forecast': None,
                        'end_date_forecast': None,
                        'completion_status': None,
                        'responsible_person': None,
                    },

                'constant':
                    {
                        'name': None
                    }
            }
        }

        # WP Properties User-Defined
        self.additional_ppts = {}


class WPScheduler(WorkPackage):
    def __init__(self, wp_id):
        super().__init__(wp_id)

        # Scheduling Properties - Cumulative
        self.predecessors = []  # {WP ids, connection type, lag}
        self.successors = []  # {WP ids, connection type, lag}


class WPResource(WorkPackage):
    def __init__(self, wp_id):
        super().__init__(wp_id)

        # Resource Properties - Cumulative
        self.required_resource_human = None  # {str from list, amount(hrs)}
        self.required_resource_material = None  # {str from list, amount(units)}


class WPQuality(WorkPackage):
    def __init__(self, wp_id):
        super().__init__(wp_id)

        # Quality Properties - Cumulative
        self.quality_criteria = []  # {str, bool}


class WPAttachment(WorkPackage):
    def __init__(self, wp_id):
        super().__init__(wp_id)

        # Resource Properties - Cumulative
        self.attachments = []


class WorkPackageTable:
    def __init__(self, setup_parameters):
        self.wp_table = self.fetch_work_package_table(setup_parameters)

    def fetch_work_package_table(self, setup_parameters):
        # call to the database
        return pd.DataFrame()

    def get_cumulative_val(self, wp_id, col_name):
        return None

    def get_val(self, wp_id, col_name):
        return None

    def add_work_package(self, new_wp: WorkPackage):
        pass
