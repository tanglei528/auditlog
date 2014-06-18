from oslo.config import cfg
from pecan import hooks


class ConfigHook(hooks.PecanHook):
    """Attach the configuration object to the request
    so controllers can get to it.
    """

    def before(self, state):
        state.request.cfg = cfg.CONF


class DBHook(hooks.PecanHook):

    def __init__(self, storage_connection):
        self.storage_connection = storage_connection

    def before(self, state):
        state.request.storage_conn = self.storage_connection
