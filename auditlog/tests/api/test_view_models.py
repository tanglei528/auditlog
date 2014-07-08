import unittest
import wsme.types as wtypes

from auditlog.api.model import view_models as vm
from auditlog.tests.api import test_data


class TestAuditLog(unittest.TestCase):

    def test_eq_with_empty_object(self):
        l1 = vm.AuditLog()
        l2 = vm.AuditLog()
        self.assertEqual(l1, l1)
        self.assertTrue(l1 == l1)
        self.assertEqual(l1, l2)
        self.assertTrue(l1 == l2)

    def test_eq_with_nonempty_object(self):
        l1 = vm.AuditLog(id='l1')
        another_l1 = vm.AuditLog(id='l1')
        l2 = vm.AuditLog(**{'id': 'l2'})
        self.assertEqual(l1, l1)
        self.assertTrue(l1 == l1)
        self.assertEqual(l1, another_l1)
        self.assertTrue(l1 == another_l1)
        self.assertTrue(l1 != l2)

    def test_eq_return_false(self):
        l1 = vm.AuditLog(id='l1')
        self.assertFalse(l1 == 'l1')
        self.assertFalse(l1 is None)
        self.assertFalse(l1 == wtypes.Unset)

    def test_from_model(self):
        one = test_data.one
        expect = vm.AuditLog(id=one.id, user_id=one.user_id,
                             tenant_id=one.tenant_id, rid=one.rid,
                             path=one.path, method=one.method,
                             status_code=one.status_code,
                             begin_at=one.begin_at, end_at=one.end_at,
                             content=one.content)
        actual = vm.AuditLog.from_model(one)
        self.assertEqual(expect, actual)


class TestPaginator(unittest.TestCase):

    def test_constructor(self):
        actual = vm.Paginator(size=1)
        self.assertEqual(1, actual.size)

    def test_eq_return_true(self):
        actual = vm.Paginator()
        self.assertTrue(actual == actual)
        actual2 = vm.Paginator()
        self.assertTrue(actual == actual2)

    def test_eq_return_false(self):
        p1 = vm.Paginator(size=1)
        p2 = vm.Paginator(size=2)
        self.assertFalse(p1 == p2)
        self.assertFalse(p1 == '{}')
        self.assertFalse(p1 is None)
        self.assertFalse(p1 == wtypes.Unset)


class TestAuditLogPage(unittest.TestCase):

    def test_constructor(self):
        one = vm.AuditLog.from_model(test_data.one)
        actual = vm.AuditLogPage(data=[one])
        self.assertEqual(type([]), type(actual.data))
        self.assertEqual(1, len(actual.data))
        self.assertEqual(one, actual.data[0])
