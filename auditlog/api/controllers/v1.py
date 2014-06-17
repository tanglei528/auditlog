from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from auditlog.api.model import view_models as vm


class ResourcesController(rest.RestController):
    """Manages resources queries."""

    @wsme_pecan.wsexpose([vm.Resource])
    def get_all(self):
        pass


class AuditLogsController(rest.RestController):
    """Manages audit logs queries."""

    @wsme_pecan.wsexpose([vm.AuditLog], [vm.Query], int)
    def get_all(self, q=[], limit=None):
        pass

    @wsme_pecan.wsexpose(vm.AuditLog, wtypes.text)
    def get_one(self, id):
        pass


class V1Controller(object):
    """Version 1 API controller root."""

    resources = ResourcesController()
    auditlogs = AuditLogsController()
