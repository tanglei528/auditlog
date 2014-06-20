from auditlog.api.model import models
from auditlog.openstack.common import timeutils as tu

one = models.AuditLog(user_id='1', tenant_id='1', rid='1.1', method='PUT',
                      status_code=200, path='/1/1',
                      begin_at=tu.parse_isotime('2014-6-18T17:31:00'),
                      end_at=tu.parse_isotime('2014-6-18T17:32:00'),
                      content='{"foo": "bar"}')
setattr(one, 'id', 'uuid1')

two = models.AuditLog(user_id='2', tenant_id='2', rid='1.2', path='/1/2',
                      method='POST', status_code=200,
                      begin_at=tu.parse_isotime('2014-6-18T17:33:00'),
                      end_at=tu.parse_isotime('2014-6-18T17:34:00'),
                      content='{"foo": "bar"}')
setattr(two, 'id', 'uuid2')

all = [one, two]
