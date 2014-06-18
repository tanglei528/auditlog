import logging
import pecan

from auditlog.api.controllers import v1


LOG = logging.getLogger(__name__)


class RootController(object):

    v1 = v1.V1Controller()

    @pecan.expose('json')
    def index(self):
        LOG.info("index()")
        return dict()
