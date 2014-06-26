from mox import Func
from mox import In

from auditlog.api.model import models as m
from auditlog.api.model import view_models as vm
from auditlog.api import tests
from auditlog.api.tests import test_data
from auditlog.openstack.common.fixture import mockpatch as oslo_mock
from auditlog.openstack.common import timeutils


class TestRootController(tests.FunctionalTest):
    """Functional test case for RootController."""
    def test_get(self):
        res = self.app.get('/')
        self.assertTrue(res.status_int == 200)


class TestAuditLogsController(tests.FunctionalTest):
    """Functional test case for AuditLogsController."""
    def setUp(self):
        super(TestAuditLogsController, self).setUp()
        self.url = '/v1/auditlogs'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=(None, None)))

    def _verify_audit_logs(self, expects, json):
        self.assertEqual(len(expects), len(json))
        for i, v in enumerate(expects):
            expect = vm.AuditLog.from_model(v)
            ob = json[i]
            # datetime attribute in json has string type, convert back
            dt_begin = timeutils.parse_isotime(ob['begin_at'])
            dt_end = timeutils.parse_isotime(ob['end_at'])
            del ob['begin_at']
            del ob['end_at']
            actual = vm.AuditLog(begin_at=dt_begin, end_at=dt_end, **ob)
            self.assertEqual(expect, actual)

    def _verify_paginator(self, expect, json):
        actual = vm.Paginator(**json)
        self.assertEqual(vm.Paginator.from_model(expect), actual)

    def test_get_all_return_data_and_paginator(self):
        """should return datas and paginator."""
        expect = ([], m.Paginator())
        self.storage_conn.get_auditlogs_paginated([], -1, None)\
            .AndReturn(expect)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertTrue(res.json['data'] is not None)
        self.assertTrue(res.json['paginator'] is not None)

    def test_get_all_success(self):
        """should return all auditlogs."""
        all = (test_data.all, m.Paginator())
        self.storage_conn.get_auditlogs_paginated([], -1, None)\
            .AndReturn(all)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self.assertTrue(res.json['data'] is not None)
        self._verify_audit_logs(test_data.all, res.json['data'])

    def test_get_all_with_paginated_success(self):
        """should return one page auditlogs and paginator."""
        all = test_data.all
        mp = m.Paginator(size=1, marker=all[0].id, total=len(all),
                         count=len(all), first=all[0].id, next=all[1].id,
                         last=all[-1].id)
        result = (all[:1], mp)
        self.storage_conn.get_auditlogs_paginated([], 1, None)\
            .AndReturn(result)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url, {'limit': 1})
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self._verify_audit_logs(all[:1], res.json['data'])
        self._verify_paginator(mp, res.json['paginator'])

    def test_get_all_with_mark_paginated_success(self):
        """should return one page auditlogs from marker and paginator."""
        all = test_data.all
        mp = m.Paginator(size=1, marker=all[1].id, total=len(all),
                         count=len(all), first=all[0].id, previous=all[0].id,
                         last=all[-1].id)
        result = (all[1:1], mp)
        self.storage_conn.get_auditlogs_paginated([], 1, all[1].id)\
            .AndReturn(result)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url, {'limit': 1, 'marker': all[1].id})
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self._verify_audit_logs(all[1:1], res.json['data'])
        self._verify_paginator(mp, res.json['paginator'])

    def test_get_all_return_empty(self):
        mp = m.Paginator(-1)
        self.storage_conn.get_auditlogs_paginated([], -1, None)\
            .AndReturn(([], mp))
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self._verify_audit_logs([], res.json['data'])
        self._verify_paginator(mp, res.json['paginator'])

    def _check_queries(self, expects, qs):
        self.assertEqual(len(expects), len(qs))
        for i, query in enumerate(expects):
            q = qs[i]
            self.assertEqual(query.field, q.field)
            self.assertEqual(query.op, q.op)
            self.assertEqual(query.value, q.value)
            self.assertEqual(query.type, q.type)
            return True

    def test_get_all_with_query(self):
        query = vm.Query(field='user_id', op='eq', value='1', type='string')
        self.storage_conn.get_auditlogs_paginated(
            Func(lambda q: self._check_queries([query], q)), -1, None
        ).AndReturn(([], m.Paginator()))
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url, {'q.field': query.field,
                                      'q.op': query.op,
                                      'q.value': query.value,
                                      'q.type': query.type})
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_all_with_queries(self):
        queries = [
            vm.Query(field='user_id', op='eq', value='1', type='string'),
            vm.Query(field='tenant_id', op='eq', value='1', type='string')
        ]
        self.storage_conn.get_auditlogs_paginated(
            Func(lambda q: self._check_queries(queries, q)), -1, None
        ).AndReturn(([], m.Paginator()))
        self.conn_mock.ReplayAll()

        params = []
        for each in queries:
            params.append('q.field=' + each.field)
            params.append('q.op=' + each.op)
            params.append('q.value=' + each.value)
            params.append('q.type=' + each.type)

        res = self.app.get(self.url + '?' + '&'.join(params))
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_one(self):
        """should return the audit log in json with the given id."""
        log = test_data.one
        self.storage_conn.get_auditlog_by_id(log.id).AndReturn(log)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url + '/' + log.id)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self._verify_audit_logs([log], [res.json])

    def test_get_not_existed_return_404(self):
        """should return 404."""
        self.storage_conn.get_auditlog_by_id('not-existed').AndReturn(None)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url + '/' + 'not-existed', expect_errors=True)
        self.assertEqual(404, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self.assertEqual('The resource could not be found.',
                         res.json['faultstring'])


class TestResourcesController(tests.FunctionalTest):
    """Functional test case for ResourcesController."""
    def setUp(self):
        super(TestResourcesController, self).setUp()
        self.url = '/v1/resources'

    def test_get_all_success(self):
        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self.assertEqual(len(m.Resource.dict), len(res.json))
        for each in res.json:
            self.assertTrue(each['rid'] is not None)
            self.assertTrue(each['name'] is not None)


class TestAuditLogsControllerWithACL(tests.FunctionalTest):
    """Functional test case for AuditLogsController with access controll."""
    def setUp(self):
        super(TestAuditLogsControllerWithACL, self).setUp()
        self.url = '/v1/auditlogs'

    def test_get_all_enforce_filter_by_tenant_id(self):
        expect_creds = 'fake_user_id', 'fake_tenant_id'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))
        tenant_query = vm.Query(field='tenant_id', op='eq',
                                value=expect_creds[1], type='string')
        self.storage_conn.get_auditlogs_paginated(In(tenant_query), -1, None)\
            .AndReturn(([], m.Paginator()))
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_all_enforce_filter_by_user_id(self):
        expect_creds = 'fake_user_id', 'fake_tenant_id'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))
        user_query = vm.Query(field='user_id', op='eq',
                              value=expect_creds[0], type='string')
        self.storage_conn.get_auditlogs_paginated(In(user_query), -1, None)\
            .AndReturn(([], m.Paginator()))
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url)
        self.assertEqual(200, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_all_filter_by_invalid_tenant_id_return_401(self):
        expect_creds = 'fack_user_id', 'fake_tenant_id'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))

        res = self.app.get(self.url, {'q.field': 'tenant_id',
                                      'q.op': 'eq',
                                      'q.value': 'invalid_tenant_id',
                                      'q.type': 'string'},
                           expect_errors=True)
        self.assertEqual(401, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_all_filter_by_invalid_user_id_return_401(self):
        expect_creds = 'fack_user_id', 'fake_tenant_id'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))

        res = self.app.get(self.url, {'q.field': 'user_id',
                                      'q.op': 'eq',
                                      'q.value': 'invalid_user_id',
                                      'q.type': 'string'},
                           expect_errors=True)
        self.assertEqual(401, res.status_int)
        self.assertEqual('application/json', res.content_type)

    def test_get_one_with_invalid_tenant_id_return_401(self):
        expect_creds = '1', 'fake_tenant_id'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))

        log = test_data.one
        self.storage_conn.get_auditlog_by_id(log.id).AndReturn(log)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url + '/' + log.id, expect_errors=True)
        self.assertEqual(401, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self.assertEqual(u'Not Authorized to access project fake_tenant_id',
                         res.json['faultstring'])

    def test_get_one_with_invalid_user_id_return_401(self):
        expect_creds = 'fake_user_id', '1'
        self.useFixture(
            oslo_mock.Patch('auditlog.api.acl.get_limited_to',
                            return_value=expect_creds))

        log = test_data.one
        self.storage_conn.get_auditlog_by_id(log.id).AndReturn(log)
        self.conn_mock.ReplayAll()

        res = self.app.get(self.url + '/' + log.id, expect_errors=True)
        self.assertEqual(401, res.status_int)
        self.assertEqual('application/json', res.content_type)
        self.assertEqual(u'Not Authorized to access for user fake_user_id',
                         res.json['faultstring'])
