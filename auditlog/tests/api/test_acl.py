from auditlog.api import acl
from auditlog import tests


class TestAcl(tests.FunctionalTest):
    """Unit tests for ACL."""
    def test_get_limited_to_with_admin(self):
        headers = {'X-User-Id': 'fake_user_1',
                   'X-Project-Id': 'fake_tenant_1',
                   'X-Roles': 'admin,_member_'}
        expect = (None, None)
        actual = acl.get_limited_to(headers)
        self.assertEqual(expect, actual)

    def test_get_limited_to_with_regular_user(self):
        headers = {'X-User-Id': 'fake_user_1',
                   'X-Project-Id': 'fake_tenant_1'}
        expect = ('fake_user_1', 'fake_tenant_1')
        actual = acl.get_limited_to(headers)
        self.assertEqual(expect, actual)
