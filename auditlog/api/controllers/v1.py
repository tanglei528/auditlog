import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from auditlog.api.model import models as m
from auditlog.api.model import view_models as vm


class ResourcesController(rest.RestController):
    """Manages resources queries."""

    @wsme_pecan.wsexpose([vm.Resource])
    def get_all(self):
        return [vm.Resource.from_model(r)
                for r in m.Resource.get_resource_list()]


class AuditLogsController(rest.RestController):
    """Manages audit logs queries."""

    @wsme_pecan.wsexpose(vm.AuditLogPage,
                         [vm.Query], int, str)
    def get_all(self, q=[], limit=-1, marker=None):
        logs, paginator = pecan.request.storage_conn.get_auditlogs_paginated(
            q, limit, marker
        )
        return vm.AuditLogPage(data=[vm.AuditLog.from_model(l) for l in logs],
                               paginator=vm.Paginator.from_model(paginator))

    @wsme_pecan.wsexpose(vm.AuditLog, wtypes.text)
    def get_one(self, id):
        log = pecan.request.storage_conn.get_auditlog_by_id(id)
        if log is None:
            pecan.abort(404)
        return vm.AuditLog.from_model(log)


class V1Controller(object):
    """Version 1 API controller root."""

    resources = ResourcesController()
    auditlogs = AuditLogsController()
