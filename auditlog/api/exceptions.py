import pecan
import wsme

from auditlog.openstack.common.gettextutils import _  # noqa


class ClientSideError(wsme.exc.ClientSideError):
    def __init__(self, error, status_code=400):
        pecan.response.translatable_error = error
        super(ClientSideError, self).__init__(error, status_code)


class EntityNotFound(ClientSideError):
    def __init__(self, entity, id):
        super(EntityNotFound, self).__init__(
            _("%(entity)s %(id)s Not Found") % {'entity': entity,
                                                'id': id},
            status_code=404)


class ProjectNotAuthorized(ClientSideError):
    def __init__(self, id, aspect='project'):
        params = dict(aspect=aspect, id=id)
        super(ProjectNotAuthorized, self).__init__(
            _("Not Authorized to access %(aspect)s %(id)s") % params,
            status_code=401)


class AccessNotAuthorized(ClientSideError):
    def __init__(self, id, aspect='user'):
        params = dict(aspect=aspect, id=id)
        super(AccessNotAuthorized, self).__init__(
            _("Not Authorized to access for %(aspect)s %(id)s") % params,
            status_code=401)
