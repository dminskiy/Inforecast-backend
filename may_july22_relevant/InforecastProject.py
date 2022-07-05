import warnings
from InforecastTracker import InforecastTracker
import os
from typing import List


PROJECTS_BASE_DIR = '/test_dir/projects'


class InforecastProject:
    def __int__(self, name):
        self._trackers: List[InforecastTracker] = []
        self.name: str = name
        self.dir: str = os.path.join(PROJECTS_BASE_DIR, name)

    def init(self):
        '''
        Initialise from scratch, assuming project with this name should not exist
        :return: True on success, False otherwise
        '''

        if os.path.isdir(self.dir):
            warnings.warn(f'Cannot initialise the project directory as a project with the same name exists already: '
                          f'{self.name}')
            return False

        os.makedirs(self.dir)

    def add_tracker(self):
        # init tracker
        pass