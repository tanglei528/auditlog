from auditlog.api.model import view_models as vm
from auditlog.api import tests
from auditlog.openstack.common import timeutils

VALID_TOKEN = '4562138218392831'
VALID_TOKEN2 = '4562138218392832'


class FakeMemcache(object):
    @staticmethod
    def get(key):
        if key == "tokens/%s" % VALID_TOKEN:
            dt = timeutils.utcnow() + datetime.timedelta(minutes=5)
            return json.dumps(({'access': {
                'token': {'id': VALID_TOKEN},
                'user': {
                    'id': 'user_id1',
                    'name': 'user_name1',
                    'tenantId': '123i2910',
                    'tenantName': 'mytenant',
                    'roles': [
                        {'name': 'admin'},
                    ]},
            }}, timeutils.isotime(dt)))
        if key == "tokens/%s" % VALID_TOKEN2:
            dt = timeutils.utcnow() + datetime.timedelta(minutes=5)
            return json.dumps(({'access': {
                'token': {'id': VALID_TOKEN2},
                'user': {
                    'id': 'user_id2',
                    'name': 'user-good',
                    'tenantId': 'project-good',
                    'tenantName': 'goodies',
                    'roles': [
                        {'name': 'Member'},
                    ]},
            }}, timeutils.isotime(dt)))

    @staticmethod
    def set(key, value, **kwargs):
        pass


class TestConnection(tests.IntegrationTest):

    def setUp(self):
        super(TestConnection, self).setUp()
        import pdb; pdb.set_trace()
        self.url = '/v1/auditlogs'

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
        return super(TestConnection, self).get_json(path,
                                                expect_errors=expect_errors,
                                                headers=headers,
                                                q=q,
                                                **params)

    def test_get_all_with_querie(self):
        expect_errors = False
        headers = {"X-User-Id": "fake_user_1",
                   "X-Project-Id": "fake_tenant_1",
                   "X-Roles": "admin",
                   "X-Tenant-Name": "admin",
                  }
        query = [{'field': 'project_id',
                  'value': 'project-good',
                  'op': 'eq',
                  'type': 'string'
                 }]
        import pdb; pdb.set_trace()
        #data = self.get_json(self.url, expect_errors, headers, query)
        data = self.app.get(self.url, query[0], expect_errors=expect_errors, headers=headers)
        