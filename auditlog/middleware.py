import logging

from oslo.config import cfg

#from nova.openstack.common import log as logging
from nova import wsgi as base


#from auditlog.openstack.common.middleware import base
from auditlog.api.model import models
from auditlog.api.model import resource_models as vm
from auditlog.openstack.common import timeutils
from auditlog.storage import impl_mongodb

LOG = logging.getLogger("nova.api.auth")


class AuditMiddleware(base.Middleware):
    """store POST/PUT/DELETE api request for audit."""

    def __init__(self, application, audit_methods='POST,PUT,DELETE'):

        super(AuditMiddleware, self).__init__(application)
        self._audit_methods = audit_methods.split(",")
        self.connection = impl_mongodb.MongoDBStorage().get_connection(cfg.CONF)

    def process_request(self, req):
        _need_audit = req.method in self._audit_methods
        if _need_audit:
           user_id = req.headers.get('X-User-Id','unknown')
           tenant_id = req.headers.get('X-Tenant-Id','unknown')
           path = req.path
           try:
               rid = vm.Resource.parse_url(path).rid
           except:
               rid = None
           method = req.method
           status_code = None
           begin_at = timeutils.utcnow()
           end_at = None
           content = req.body
           self._log = models.AuditLog(user_id, tenant_id, rid, path, method,
                           status_code, begin_at, end_at, 
                           content)
        else:
            self._log = None

    def process_response(self, response):
        
        if self._log is not None:
           self._log.status_code = response.status_int
           self._log.end_at = timeutils.utcnow()
           self._store_log(self._log)
           self._log = None
        return response

    def _store_log(self, log):
        try:
            self.connection.create_auditlog(log.as_dict())
        except Exception as e:
            LOG.error("Store audit log error : %s",e)
