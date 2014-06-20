from auditlog.api.model import resource_models as resource


class TestResource(resource.Resource):
    def test_parse_url(self):
        r = resource.Resource.parse_url("/v2.0/networks")
        assert r.rid == "1.2.1"
        assert r.rname == "NetWorks"
        r = resource.Resource.parse_url("/v2/{tenant}/servers/{serve}/action")
        assert r.rid == "2.2.7"
        assert r.rname == "Update status"
        r = resource.Resource.parse_url("/v2/{tenant_id}/flavors/{flavor_id}")
        assert r.rid == "2.2.1"
        assert r.rname == "Flavors"
        r = resource.Resource.parse_url("/v2/{tenant_id}/volumes/{volume_id}")
        assert r.rid == "3.2.1"
        assert r.rname == "Volumes"
        r = resource.Resource.parse_url("/v2/images/{image_id}")
        assert r.rid == "4.2.1"
        assert r.rname == "Images"

    def test_resource_list(self):
        list = resource.Resource.get_resource_list()
        assert len(list) == 41
