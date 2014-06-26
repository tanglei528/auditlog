import pecan
from pecan import rest
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from auditlog.api import acl
from auditlog.api import exceptions
from auditlog.api.model import models as m
from auditlog.api.model import view_models as vm
from auditlog.openstack.common import log

LOG = log.getLogger(__name__)


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
        authed_user_id, authed_tenant_id = acl.get_limited_to(pecan.request)
        if authed_user_id is not None:
            valid, id = self._validate_queries(q, 'user_id', authed_user_id)
            if not valid:
                raise exceptions.AccessNotAuthorized(id)
        if authed_tenant_id is not None:
            valid, id = self._validate_queries(q, 'tenant_id',
                                               authed_tenant_id)
            if not valid:
                raise exceptions.ProjectNotAuthorized(id)

        logs, paginator = pecan.request.storage_conn.get_auditlogs_paginated(
            q, limit, marker
        )
        logs = logs if logs else []
        rp = vm.Paginator.from_model(paginator) if paginator else None
        return vm.AuditLogPage(data=[vm.AuditLog.from_model(l) for l in logs],
                               paginator=rp)

    @wsme_pecan.wsexpose(vm.AuditLog, wtypes.text)
    def get_one(self, id):
        log = pecan.request.storage_conn.get_auditlog_by_id(id)
        if log is None:
            pecan.abort(404)
        return vm.AuditLog.from_model(log)

    def _validate_queries(self, queries, field, value):
        """Validate and update the queries to enforce auth limit
        :return: a tuple (result, id), return (True, None) if valid,
                 or return (False, invalid_value)
        """
        has_enforced = False
        for each in queries:
            if each.field == field:
                if each.value != value:
                    LOG.error("Query by %s '%s' is invalid", field, each.value)
                    return False, each.value
                else:
                    has_enforced = True
        if not has_enforced:
            LOG.info("Enforce query %s to '%s'.", field, value)
            q = vm.Query(field=field, op='eq', value=value,
                         type='string')
            queries.append(q)
        return True, None


class V1Controller(object):
    """Version 1 API controller root."""

    resources = ResourcesController()
    auditlogs = AuditLogsController()
