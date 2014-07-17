from auditlog.api.model import view_models as vm
from auditlog.openstack.common import timeutils
from auditlog import tests
from auditlog.tests.storage import test_data


class TestStorageMongoImplement(tests.IntegrationTest):

    def setUp(self):
        super(TestStorageMongoImplement, self).setUp()
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
        return super(TestStorageMongoImplement, self).get_json(
            path,
            expect_errors=expect_errors,
            headers=headers,
            q=q,
            **params)

    def test_get_all_with_admin_role(self):
        expect_errors = False
        headers = {"X-User-Id": "fake_user_1",
                   "X-Project-Id": "fake_tenant_1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        data = self.get_json(self.url, expect_errors, headers)
        self._verify_audit_logs(test_data.all, data['data'])

    def test_get_all_with_admin_role_and_filter(self):
        expect_errors = False
        headers = {"X-User-Id": "fake_user_1",
                   "X-Project-Id": "fake_tenant_1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin", }
        query = [{'field': 'tenant_id',
                  'value': test_data.one.tenant_id,
                  'op': 'eq',
                  'type': 'string'}]
        data = self.get_json(self.url, expect_errors, headers, query)
        self._verify_audit_logs([test_data.one], data['data'])
