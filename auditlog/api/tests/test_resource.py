import operator
import unittest

from auditlog.api.model import models as resource


class TestResource(unittest.TestCase):
    def test_parse_url(self):
        r = resource.Resource.parse_url("/v2.0/networks")
        self.assertTrue(str(r.rid) == "1.2.1")
        self.assertTrue(str(r.name) == "NetWorks")
        r = resource.Resource.parse_url("/v2/{tenant}/servers/{serve}/action")
        self.assertEqual(str(r.rid), "2.2.7")
        self.assertTrue(str(r.name) == "Update server")
        r = resource.Resource.parse_url("/v2/{tenant_id}/flavors/{flavor_id}")
        self.assertTrue(str(r.rid) == "2.2.1")
        self.assertTrue(str(r.name) == "Flavors")
        r = resource.Resource.parse_url("/v2/{tenant_id}/volumes/{volume_id}")
        self.assertTrue(str(r.rid) == "3.2.1")
        self.assertTrue(str(r.name) == "Volumes")
        r = resource.Resource.parse_url("/v2/images/{image_id}")
        self.assertTrue(str(r.rid) == "4.2.1")
        self.assertTrue(str(r.name) == "Images")

    def test_resource_list(self):
        list = resource.Resource.get_resource_list()
        self.assertTrue(len(list) == 37)
        sorted_list = sorted(list, key=operator.attrgetter('rid'))
        self.assertEqual(sorted_list, list)


class TestResourceId(unittest.TestCase):
    def test_str(self):
        rid = resource.ResourceId('1.1')
        self.assertEqual('1.1', str(rid))

    def test_lt_gt(self):
        rid1 = resource.ResourceId('1.1')
        rid2 = resource.ResourceId('2.1')
        self.assertTrue(rid1.__lt__(rid2))
        self.assertTrue(rid1 < rid2)
        self.assertFalse(rid2 < rid1)
        self.assertTrue(rid2.__gt__(rid1))
        self.assertTrue(rid2 > rid1)
        rid3 = resource.ResourceId('1')
        rid4 = resource.ResourceId('2')
        self.assertTrue(rid3.__lt__(rid4))
        self.assertTrue(rid3 < rid4)
        self.assertFalse(rid4 < rid3)
        self.assertTrue(rid4.__gt__(rid3))
        self.assertTrue(rid4 > rid3)
        rid5 = resource.ResourceId('1.1.1')
        self.assertTrue(rid1.__lt__(rid5))
        self.assertTrue(rid1 < rid5)
        self.assertTrue(rid5.__gt__(rid1))
        self.assertTrue(rid5 > rid1)
        self.assertTrue(rid3.__lt__(rid5))
        self.assertTrue(rid3 < rid5)
        self.assertTrue(rid5.__gt__(rid3))
        self.assertTrue(rid5 > rid3)

    def test_ge_le(self):
        rid1 = resource.ResourceId('1.1')
        rid2 = resource.ResourceId('2.1')
        self.assertTrue(rid1.__le__(rid2))
        self.assertTrue(rid1 <= rid2)
        self.assertFalse(rid2 <= rid1)
        self.assertTrue(rid2.__ge__(rid1))
        self.assertTrue(rid2 >= rid1)
        rid3 = resource.ResourceId('1')
        rid4 = resource.ResourceId('2')
        self.assertTrue(rid3.__le__(rid4))
        self.assertTrue(rid3 <= rid4)
        self.assertFalse(rid4 <= rid3)
        self.assertTrue(rid4.__ge__(rid3))
        self.assertTrue(rid4 >= rid3)
        rid5 = resource.ResourceId('1.1.1')
        self.assertTrue(rid1.__le__(rid5))
        self.assertTrue(rid1 <= rid5)
        self.assertTrue(rid5.__ge__(rid1))
        self.assertTrue(rid5 >= rid1)
        self.assertTrue(rid3.__le__(rid5))
        self.assertTrue(rid3 <= rid5)
        self.assertTrue(rid5.__ge__(rid3))
        self.assertTrue(rid5 >= rid3)
        rid6 = resource.ResourceId('1.1.1')
        self.assertTrue(rid5.__le__(rid6))
        self.assertTrue(rid5 <= rid6)
        self.assertTrue(rid5.__ge__(rid6))
        self.assertTrue(rid5 >= rid6)

    def test_eq_ne(self):
        rid1 = resource.ResourceId('1.1')
        self.assertEqual(rid1, rid1)
        self.assertTrue(rid1.__eq__(rid1))
        self.assertTrue(rid1 == rid1)
        rid2 = resource.ResourceId('1.1')
        self.assertEqual(rid1, rid2)
        self.assertTrue(rid2.__eq__(rid1))
        self.assertTrue(rid2 == rid1)
        rid3 = resource.ResourceId('1.2')
        self.assertNotEqual(rid1, rid3)
        self.assertTrue(rid1.__ne__(rid3))
        self.assertTrue(rid1 != rid3)

    def test_sort(self):
        l = [resource.ResourceId('1.1'),
             resource.ResourceId('1.2'),
             resource.ResourceId('1.3')]
        sl = sorted(l)
        self.assertEqual(l, sl)
        rl = sorted(l, reverse=True)
        self.assertNotEqual(l, rl)
        for i, expect in enumerate(l):
            self.assertEqual(expect, rl[-i - 1])

        r1 = resource.ResourceId('1.2.5')
        r2 = resource.ResourceId('2.2.1')
        r3 = resource.ResourceId('1.2.3')
        self.assertTrue(r3 < r1)
        self.assertTrue(r1 < r2)
        l2 = [r1,
              r2,
              r3]
        l2.sort()
        self.assertEqual(r3, l2[0])
        self.assertEqual(r1, l2[1])
        self.assertEqual(r2, l2[2])
