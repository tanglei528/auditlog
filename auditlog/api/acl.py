# -*- encoding: utf-8 -*-
#
# Copyright © 2012 New Dream Network, LLC (DreamHost)
#
# Author: Doug Hellmann <doug.hellmann@dreamhost.com>
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

"""Access Control Lists (ACL's) control access the API server."""

import functools
import pecan

from auditlog.api import exceptions
from auditlog.openstack.common import policy
from keystoneclient.middleware import auth_token
from oslo.config import cfg


_ENFORCER = None
OPT_GROUP_NAME = 'keystone_authtoken'


def register_opts(conf):
    """Register keystoneclient middleware options
    """
    conf.register_opts(auth_token.opts,
                       group=OPT_GROUP_NAME)
    auth_token.CONF = conf


register_opts(cfg.CONF)


def install(app, conf):
    """Install ACL check on application."""
    return auth_token.AuthProtocol(app,
                                   conf=dict(conf.get(OPT_GROUP_NAME)))


def get_limited_to(headers):
    """Return the user and project the request should be limited to.

    :param headers: HTTP headers dictionary
    :return: A tuple of (user, project), set to None if there's no limit on
    one of these.

    """
    global _ENFORCER
    if not _ENFORCER:
        _ENFORCER = policy.Enforcer()
    if not _ENFORCER.enforce('context_is_admin',
                             {},
                             {'roles': headers.headers.get('X-Roles',
                                                           "").split(",")}):
        return (headers.headers.get('X-User-Id', 'Unkown'),
                headers.headers.get('X-Project-Id', 'Unknown'))
    return None, None


def get_limited_to_project(headers):
    """Return the project the request should be limited to.

    :param headers: HTTP headers dictionary
    :return: A project, or None if there's no limit on it.

    """
    return get_limited_to(headers)[1]


def requires_admin(func):

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        usr_limit, proj_limit = get_limited_to(pecan.request.headers)
        # If User and Project are None, you have full access.
        if usr_limit and proj_limit:
            raise exceptions.ProjectNotAuthorized(proj_limit)
        return func(*args, **kwargs)

    return wrapped
