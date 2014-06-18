import os
import pecan
from pecan import testing
import unittest

__all__ = ['FunctionalTest']


class FunctionalTest(unittest.TestCase):
    """Used for functional tests where you need to test your
    literal application and its integration with the framework.
    """

    def setUp(self):
        self.app = testing.load_test_app(os.path.join(
            os.path.dirname(__file__),
            'config.py'
        ))

    def tearDown(self):
        pecan.set_config({}, overwrite=True)
