import sys

from oslo.config import cfg
import pecan

from auditlog.api import hooks
from auditlog.api import model
from auditlog.openstack.common import log
from auditlog import storage

cfg.CONF(args=sys.argv[3:],
         project='auditlog')
log.setup('auditlog')
LOG = log.getLogger(__name__)


def setup_app(config):

    model.init_model()
    app_conf = dict(config.app)

    # FIXME: Replace DBHook with hooks.TransactionHook
    app_hooks = [hooks.ConfigHook(),
                 hooks.DBHook(
                     storage.get_connection(cfg.CONF),
                 )]
    if 'hooks' in app_conf.keys():
        app_hooks = app_conf['hooks']
        LOG.info("Use hooks %s", app_hooks)
        del app_conf['hooks']

    return pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        hooks=app_hooks,
        **app_conf
    )
