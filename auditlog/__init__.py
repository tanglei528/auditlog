from oslo.config import cfg

# Register options for the service
API_SERVICE_OPTS = [
    cfg.IntOpt('port',
               default=8800,
               help='The port for the auditlog API server.',
               ),
    cfg.StrOpt('host',
               default='0.0.0.0',
               help='The listen IP for the auditlog API server.',
               ),
]

CONF = cfg.CONF
opt_group = cfg.OptGroup(name='api',
                         title='Options for the auditlog-api service')
CONF.register_group(opt_group)
CONF.register_opts(API_SERVICE_OPTS, opt_group)
