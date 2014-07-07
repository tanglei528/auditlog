import os
import uuid
import warnings

import six

import mox
import pecan
from pecan import testing

from auditlog.api import hooks as cust_hooks
from auditlog.api.tests import base as test_base
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
    PATH_PREFIX = ''

    def setUp(self):
        super(IntegrationTest, self).setUp()
        self.database_connection=MongoDBFakeConnectionUrl()
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
                message='.*you must provide a username and password.Authentication required*')
            self.conn = storage.get_connection(self.CONF)
        self.conn.upgrade()

        service.prepare_service([])
        self.CONF.set_override('policy_file',
                               self.get_path('etc/auditlog/policy.json'))
        self.app = testing.load_test_app(os.path.join(
            os.path.dirname(__file__),
            self.CONFIG_FILE,
        ))

    def tearDown(self):
        #self.conn.clear()
        self.conn = None
        pecan.set_config({}, overwrite=True)
        super(IntegrationTest, self).tearDown()

    def get_json(self, path, expect_errors=False, headers=None,
                 extra_environ=None, q=[], groupby=[], status=None,
                 override_params=None, **params):
        """Sends simulated HTTP GET request to Pecan test app.

        :param path: url path of target service
        :param expect_errors: boolean value whether an error is expected based
                              on request
        :param headers: A dictionary of headers to send along with the request
        :param extra_environ: A dictionary of environ variables to send along
                              with the request
        :param q: list of queries consisting of: field, value, op, and type
                  keys
        :param groupby: list of fields to group by
        :param status: Expected status code of response
        :param override_params: literally encoded query param string
        :param params: content for wsgi.input of request
        """
        full_path = self.PATH_PREFIX + path
        if override_params:
            all_params = override_params
        else:
            query_params = {'q.field': [],
                            'q.value': [],
                            'q.op': [],
                            'q.type': [],
                            }
            for query in q:
                for name in ['field', 'op', 'value', 'type']:
                    query_params['q.%s' % name].append(query.get(name, ''))
            all_params = {}
            all_params.update(params)
            if q:
                all_params.update(query_params)
            if groupby:
                all_params.update({'groupby': groupby})
        response = self.app.get(full_path,
                                params=all_params,
                                headers=headers,
                                extra_environ=extra_environ,
                                expect_errors=expect_errors,
                                status=status)
        if not expect_errors:
            response = response.json
        return response

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


class MongoDBFakeConnectionUrl(object):

    def __init__(self):
        self.url = os.environ.get('CEILOMETER_TEST_MONGODB_URL')
        if not self.url:
            raise RuntimeError(
                "No MongoDB test URL set,"
                "export CEILOMETER_TEST_MONGODB_URL environment variable")

    def __str__(self):
        return '%(url)s' % dict(url=self.url)
