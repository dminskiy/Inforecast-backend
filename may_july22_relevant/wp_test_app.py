from other_test_scripts.WorkPackage import WPFamilyProperties, WorkPackageProperties, WorkPackage
from Table import Table
import datetime


WP_TEST_INFO = {
    'cost_baseline': 12100.5,
    'cost_forecast': 12100.5,
    'start_date_baseline': datetime.datetime.now(),
    'end_date_baseline': datetime.datetime.now() + datetime.timedelta(days=30),
    'start_date_forecast': datetime.datetime.now() + datetime.timedelta(days=5),
    'end_date_forecast': datetime.datetime.now() + datetime.timedelta(days=45),
    'completion_status': False,
    'responsible_person': 'John Thompson'
}

TABLE_PATH = '/mnt/hdd1/DM/PycharmProjects/Inforecast-backend'
TABLE_NAME = 'test_table_v0.csv'

if __name__ == '__main__':
    '''
        Creating a 'Project' - a collection of work packages
    '''
    # Project Setup
    project_properties = WorkPackageProperties().to_list()
    wp_family_properties = WPFamilyProperties().to_list()

    # For now a project is represented with a table using Table class
    wp_properties_table = Table()
    wp_properties_table.create_table(columns=project_properties, index='WPId')
    # WP Fam Table is required to keep track and have easy access to relationships between WPs
    wp_fam_table = Table()
    wp_fam_table.create_table(columns=wp_family_properties)

    work_packages_to_insert = []
    for pkg_num in range(1, 4, 1):
        # WPId: lvl.wp_number.parent_number. parent_number = full parent number inc lvl, id and its parent number
        work_package = WorkPackage()
        work_package.create(name=f'test_wp_{pkg_num}', level=0, count=pkg_num, parent=None)
        for key in WP_TEST_INFO.keys():
            work_package.set_property(ppty_name=key, val=WP_TEST_INFO[key])

        work_packages_to_insert.append(work_package)

    for wp in work_packages_to_insert:
        wp_as_row = wp.to_dict()
        wp_properties_table.insert_row(new_row=wp_as_row)

    wp_properties_table.save_table(table_path=TABLE_PATH,
                                   table_name=TABLE_NAME)

    table_indexes = wp_properties_table.index()

    for indx in table_indexes:
        work_package = WorkPackage()
        work_package.load(wp_id=indx, properties_table=wp_properties_table, relationships_table=Table())
        work_package.print()

    # TODO: Implement multi-level WP with fam_table
    # TODO: Sim multi-level WP
    # TODO: Implement WP data handling
    # TODO: Test multi-level data handling
    # TODO: Implement Quality
    # TODO: Test load_table
