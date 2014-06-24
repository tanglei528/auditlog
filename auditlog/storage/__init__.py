from auditlog.openstack.common.gettextutils import _  # noqa
from auditlog.openstack.common import log
from oslo.config import cfg
import six.moves.urllib.parse as urlparse
from stevedore import driver

LOG = log.getLogger(__name__)

STORAGE_ENGINE_NAMESPACE = 'auditlog.storage'

database_opts = [
    cfg.StrOpt('auditlog_connection',
               default='mongodb://localhost:27017/auditlog',
               help='The SQLAlchemy connection string used to connect to the '
                    'database',
               secret=True)
]

CONF = cfg.CONF
CONF.register_opts(database_opts, group="database")


def get_engine(conf):
    """Return the database engine according to configuration."""
    engine_name = urlparse.urlparse(conf.database.auditlog_connection).scheme
    LOG.debug(_('looking for %(name)r driver in %(namespace)r') % (
              {'name': engine_name,
               'namespace': STORAGE_ENGINE_NAMESPACE}))
    mgr = driver.DriverManager(STORAGE_ENGINE_NAMESPACE,
                               engine_name,
                               invoke_on_load=True)
    return mgr.driver


def get_connection(conf):
    """Return an opened connection to the database."""
    return get_engine(conf).get_connection(conf)
