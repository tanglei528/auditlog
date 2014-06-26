from auditlog.api import app
from auditlog import service


def api():
    service.prepare_service()
    srv = app.build_server()
    srv.serve_forever()
