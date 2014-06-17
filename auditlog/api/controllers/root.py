import logging

from pecan import expose, redirect
from webob.exc import status_map


LOG = logging.getLogger(__name__)

class RootController(object):

    @expose('json')
    def index(self):
        LOG.info("index()")
        return dict()
