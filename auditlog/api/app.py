import logging
import os
import socket
from wsgiref import simple_server

import netaddr
from oslo.config import cfg
import pecan

from auditlog.api import acl
from auditlog.api import hooks
from auditlog.api import model
from auditlog import config
from auditlog.openstack.common import log
from auditlog import storage

LOG = log.getLogger(__name__)

auth_opts = [
    cfg.StrOpt('auth_strategy',
               default='keystone',
               help='The strategy to use for auth: noauth or keystone.'),
    cfg.BoolOpt('enable_v1_api',
                default=True,
                help='Deploy the deprecated v1 API.'),
]

cfg.CONF.register_opts(auth_opts)


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

    app_conf['debug'] = cfg.CONF.debug
    app = pecan.make_app(
        app_conf.pop('root'),
        static_root=app_conf.get('static_root', None),
        template_path=app_conf.get('template_path', None),
        force_canonical=app_conf.get('force_canonical', True),
        hooks=app_hooks,
        guess_content_type_from_ext=False
    )

    # setup acl
    if app_conf.get('enable_acl', True):
        return acl.install(app, cfg.CONF)

    return app


def get_server_cls(host):
    """Return an appropriate WSGI server class base on provided host

    :param host: The listen host for the ceilometer API server.
    """
    server_cls = simple_server.WSGIServer
    if netaddr.valid_ipv6(host):
        # NOTE(dzyu) make sure use IPv6 sockets if host is in IPv6 pattern
        if getattr(server_cls, 'address_family') == socket.AF_INET:
            class server_cls(server_cls):
                address_family = socket.AF_INET6
    return server_cls


def build_server():
    # Build the WSGI app
    root = setup_app(config)

    # Create the WSGI server and start it
    host, port = cfg.CONF.api.host, cfg.CONF.api.port
    server_cls = get_server_cls(host)
    srv = simple_server.make_server(host, port, root, server_cls)

    LOG.info(_('Starting server in PID %s') % os.getpid())
    LOG.info(_("Configuration:"))
    cfg.CONF.log_opt_values(LOG, logging.INFO)

    if host == '0.0.0.0':
        LOG.info(_(
            'serving on 0.0.0.0:%(sport)s, view at http://127.0.0.1:%(vport)s')
            % ({'sport': port, 'vport': port}))
    else:
        LOG.info(_("serving on http://%(host)s:%(port)s") % (
                 {'host': host, 'port': port}))
    return srv
