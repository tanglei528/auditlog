import mox
import os
import pecan
from pecan import testing
import unittest

from auditlog.api import hooks as cust_hooks
from auditlog.storage import base

__all__ = ['FunctionalTest']


class FunctionalTest(unittest.TestCase):
    """Used for functional tests where you need to test your
    literal application and its integration with the framework.
    """

    CONFIG_FILE = 'config.py'

    def setUp(self):
        self.app = testing.load_test_app(os.path.join(
            os.path.dirname(__file__),
            self.CONFIG_FILE,
        ))

    def tearDown(self):
        pecan.set_config({}, overwrite=True)

DBHOOK = cust_hooks.DBHook(None)


class MoxFunctionalTest(FunctionalTest):
    """Base FunctionalTest with mocked storage connection."""

    CONFIG_FILE = 'mock_config.py'

    def setUp(self):
        super(MoxFunctionalTest, self).setUp()
        self.conn_mock = mox.Mox()
        self.storage_conn = self.conn_mock.CreateMock(base.Connection)
        DBHOOK.storage_connection = self.storage_conn

    def tearDown(self):
        super(MoxFunctionalTest, self).tearDown()
        self.conn_mock.VerifyAll()
