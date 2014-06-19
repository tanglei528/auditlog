import unittest
from auditlog.api.model.resource_models import Resource


class TestResource(unittest.TestCase):
    def test_parse_url(self):
        r = Resource(url="/v2.0/networks").parse_url()
        assert r.rid == "1.2.1"
        assert r.rname == "NetWorks"
        r = Resource(url="/v2/{tenant}/servers/{serve}/action").parse_url()
        assert r.rid == "2.2.7"
        assert r.rname == "Update status"
        r = Resource(url="/v2/{tenant_id}/flavors/{flavor_id}").parse_url()
        assert r.rid == "2.2.1"
        assert r.rname == "Flavors"
        r = Resource(url="/v2/{tenant_id}/volumes/{volume_id}").parse_url()
        assert r.rid == "3.2.1"
        assert r.rname == "Volumes"
        r = Resource(url="/v2/images/{image_id}").parse_url()
        assert r.rid == "4.2.1"
        assert r.rname == "Images"

    def test_resource_list(self):
        list = Resource().get_resource_list()
        assert len(list) == 41
