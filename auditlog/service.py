#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright © 2012-2014 eNovance <licensing@enovance.com>
#
# Author: Julien Danjou <julien@danjou.info>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from oslo.config import cfg

from auditlog.openstack.common import gettextutils
from auditlog.openstack.common.gettextutils import _  # noqa
from auditlog.openstack.common import log


def prepare_service(argv=None):
    gettextutils.install('auditlog', lazy=True)
    gettextutils.enable_lazy()
    cfg.set_defaults(log.log_opts,
                     default_log_levels=['sqlalchemy=WARN',
                                         'keystoneclient=INFO',
                                         'stevedore=INFO',
                                         'iso8601=WARN'
                                         ])
    if argv is None:
        argv = sys.argv
    cfg.CONF(argv[1:], project='auditlog')
    log.setup('auditlog')
