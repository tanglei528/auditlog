from oslo.config import cfg
import pecan

from auditlog.api import hooks
from auditlog.api import model
from auditlog import storage


def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)

    # FIXME: Replace DBHook with hooks.TransactionHook
    app_hooks = [hooks.ConfigHook(),
                 hooks.DBHook(
                     storage.get_connection(cfg.CONF),
                 )]

    return pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf
    )
