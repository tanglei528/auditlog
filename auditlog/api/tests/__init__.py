import os
import warnings

import mox
import pecan
from pecan import testing

from auditlog.api import hooks as cust_hooks
from auditlog.openstack.common.fixture import config
from auditlog.openstack.common.fixture import mockpatch as oslo_mock
from auditlog.openstack.common import test
from auditlog import service
from auditlog import storage
from auditlog.storage import base

__all__ = ['FunctionalTest']


class IntegrationTest(test.BaseTestCase):
    """Used for functional tests where you need to test your
    literal application and its integration with the framework.
    """

    CONFIG_FILE = 'config.py'

    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.database_connection = self.get_db_connection()
        if self.database_connection is None:
            self.skipTest("No connection URL set")

        self.CONF = self.useFixture(config.Config()).conf
        self.CONF([], 'auditlog')
        self.CONF.set_override('auditlog_connection',
                               str(self.database_connection),
                               group='database')
        with warnings.catch_warnings():
            warnings.filterwarnings(
                action='ignore',
                message='.*you must provide a username and password.*')
            self.conn = storage.get_connection(self.CONF)
        self.conn.upgrade()

        self.useFixture(oslo_mock.Patch('auditlog.storage.get_connection',
                                        return_value=self.conn))

        service.prepare_service([])
        self.CONF.set_override('policy_file',
                               self.get_path('etc/auditlog/policy.json'))
        self.app = testing.load_test_app(os.path.join(
            os.path.dirname(__file__),
            self.CONFIG_FILE,
        ))

    def tearDown(self):
        self.conn.clear()
        self.conn = None
        pecan.set_config({}, overwrite=True)
        super(FunctionalTest, self).tearDown()

    def get_db_connection(self):
        return 'mongodb://192.168.0.190:27017/auditlog'

DBHOOK = cust_hooks.DBHook(None)


class FunctionalTest(test.BaseTestCase):
    """Base FunctionalTest with mocked storage connection."""

    CONFIG_FILE = 'mock_config.py'

    def setUp(self):
        super(FunctionalTest, self).setUp()
        self.CONF = self.useFixture(config.Config()).conf
        self.CONF([], 'auditlog')
        self.conn_mock = mox.Mox()
        self.storage_conn = self.conn_mock.CreateMock(base.Connection)
        DBHOOK.storage_connection = self.storage_conn
        self.useFixture(oslo_mock.Patch('auditlog.storage.get_connection',
                                        return_value=self.storage_conn))

        self.app = testing.load_test_app(os.path.join(
            os.path.dirname(__file__),
            self.CONFIG_FILE,
        ))
        self.app.debug = True
        self.CONF.set_override('policy_file',
                               self.get_path('etc/auditlog/policy.json'))

    def tearDown(self):
        self.conn_mock.VerifyAll()
        self.storage_conn = None
        DBHOOK.storage_conn = None
        pecan.set_config({}, overwrite=True)
        super(FunctionalTest, self).tearDown()
