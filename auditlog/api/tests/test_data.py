from auditlog.api.model import models
from auditlog.openstack.common import timeutils as tu

one = models.AuditLog(id='uuid1', user_id='1', tenant_id='1', rid='1.1',
                      method='PUT',
                      status_code=200, path='/1/1',
                      begin_at=tu.parse_isotime('2014-6-18T17:31:00'),
                      end_at=tu.parse_isotime('2014-6-18T17:32:00'),
                      content='{"foo": "bar"}')

two = models.AuditLog(id='uuid2', user_id='2', tenant_id='2', rid='1.2',
                      path='/1/2',
                      method='POST', status_code=200,
                      begin_at=tu.parse_isotime('2014-6-18T17:33:00'),
                      end_at=tu.parse_isotime('2014-6-18T17:34:00'),
                      content='{"foo": "bar"}')

all = [one, two]
