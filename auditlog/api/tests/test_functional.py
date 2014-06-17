from auditlog.api import tests


class TestRootController(tests.FunctionalTest):

    def test_get(self):
        response = self.app.get('/')
        assert response.status_int == 200
