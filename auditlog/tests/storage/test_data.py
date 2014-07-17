from auditlog.api.model import models
from auditlog.openstack.common import timeutils as tu

one = models.AuditLog(
    id='53b0c9c6ee4d3917ee827cae',
    user_id='e728072c3931483dad4494309d18fc9f',
    tenant_id='a3ab1d350f6f465e9f60766d5d78efc2',
    rid='2.2.12',
    method='GET',
    status_code=200,
    path='/v2/a3ab1d350f6f465e9f60766d5d78efc2/os-floating-ips',
    begin_at=tu.parse_isotime('2014-6-18T17:31:00'),
    end_at=tu.parse_isotime('2014-6-18T17:32:00'),
    content='')

two = models.AuditLog(
    id='53b0c9f2ee4d3917ee827caf',
    user_id='e728072c3931483dad4494309d18fc9f',
    tenant_id='a3ab1d350f6f465e9f60766d5d78efc2',
    rid='2.2.26',
    path='/v2/a3ab1d350f6f465e9f60766d5d78efc2/servers/detail',
    method='POST',
    status_code=200,
    begin_at=tu.parse_isotime('2014-6-18T17:33:00'),
    end_at=tu.parse_isotime('2014-6-18T17:34:00'),
    content='{"foo": "bar"}')

three = models.AuditLog(
    id='53b0c9f2ee4d3917ee827cb0',
    user_id='e728072c3931483dad4494309d18fca0',
    tenant_id='a3ab1d350f6f465e9f60766d5d78efc2',
    rid='2.2.26',
    path='/v2/a3ab1d350f6f465e9f60766d5d78efc2/servers/detail',
    method='POST',
    status_code=200,
    begin_at=tu.parse_isotime('2014-6-19T17:33:00'),
    end_at=tu.parse_isotime('2014-6-19T17:34:00'),
    content='{"foo": "bar"}')

all = [one, two, three]
