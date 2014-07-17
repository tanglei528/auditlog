from auditlog.api.model import view_models as vm
from auditlog.openstack.common import timeutils
from auditlog import tests
from auditlog.tests.api import test_data
import time


class TestAuditlogImplement(tests.IntegrationTest):

    def setUp(self):
        super(TestAuditlogImplement, self).setUp()
        self.url = '/v1/auditlogs'
        for each in test_data.all:
            self.conn.create_auditlog(each)

    def _verify_audit_logs(self, expects, json):
        self.assertEqual(len(expects), len(json))
        for i, v in enumerate(expects):
            expect = vm.AuditLog.from_model(v)
            ob = json[i]
            # datetime attribute in json has string type, convert back
            dt_begin = timeutils.parse_isotime(ob['begin_at'])
            dt_end = timeutils.parse_isotime(ob['end_at'])
            ob['begin_at'] = dt_begin
            ob['end_at'] = dt_end
            fields = ['id', 'user_id', 'tenant_id', 'rid', 'path', 'method',
                      'status_code', 'begin_at', 'end_at', 'content']
            for k in fields:
                self.assertEqual(getattr(expect, k), ob[k])

    def get_json(self, path, expect_errors=False, headers=None,
                 q=[], **params):
        return super(TestAuditlogImplement, self).get_json(
            path,
            expect_errors=expect_errors,
            headers=headers,
            q=q,
            **params)

    def test_get_all_with_querie(self):
        expect_errors = False
        headers = {"X-User-Id": "1",
                   "X-Project-Id": "1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'user_id',
                  'value': test_data.one.user_id,
                  'op': 'eq',
                  'type': 'string'}]
        data = self.get_json(self.url, expect_errors, headers, query)
        self._verify_audit_logs([test_data.one], data['data'])

    def test_get_all_with_queries(self):
        expect_errors = False
        headers = {"X-User-Id": "1",
                   "X-Project-Id": "1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'user_id',
                  'value': test_data.one.user_id,
                  'op': 'eq',
                  'type': 'string'},
                 {'field': 'tenant_id',
                  'value': test_data.one.tenant_id,
                  'op': 'eq',
                  'type': 'string'}]
        data = self.get_json(self.url, expect_errors, headers, query)
        self._verify_audit_logs([test_data.one], data['data'])

    def test_get_all_with_method(self):
        expect_errors = False
        headers = {"X-User-Id": "1",
                   "X-Project-Id": "1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'method',
                  'value': test_data.one.method,
                  'op': 'eq',
                  'type': 'string'}]
        data = self.get_json(self.url, expect_errors, headers, query)
        self._verify_audit_logs([test_data.one], data['data'])

    def test_get_limited_results_with_marker(self):
        expect_errors = False
        headers = {"X-User-Id": "2",
                   "X-Project-Id": "2",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'user_id',
                  'value': test_data.two.user_id,
                  'op': 'eq',
                  'type': 'string'}]
        time.sleep(1)
        data = self.get_json(self.url + '?limit=1&marker=uuid2',
                             expect_errors, headers,
                             query)
        self._verify_audit_logs([test_data.two], data['data'])

    def test_get_limited_results(self):
        expect_errors = False
        headers = {"X-User-Id": "1",
                   "X-Project-Id": "1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'user_id',
                  'value': test_data.one.user_id,
                  'op': 'eq',
                  'type': 'string'}]
        data = self.get_json(self.url + '?limit=1', expect_errors, headers,
                             query)
        self._verify_audit_logs([test_data.one], data['data'])

    def test_get_unauthorized_entry(self):
        expect_errors = True
        headers = {"X-User-Id": "1",
                   "X-Project-Id": "1",
                   "X-Roles": "member",
                   "X-Tenant-Name": "memeber", }
        query = [{'field': 'user_id',
                  'value': test_data.two.user_id,
                  'op': 'eq',
                  'type': 'string'}]
        self.get_json(self.url, expect_errors, headers, query)
