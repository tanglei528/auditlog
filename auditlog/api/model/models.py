class Model(object):

    def as_dict(self):
        """Convert model to dict."""
        return dict([(k, getattr(self, k, None)) for k in self.fields])


class AuditLog(Model):
    """Audit Log model class."""

    fields = ['id', 'user_id', 'tenant_id', 'rid', 'path',
              'method', 'status_code', 'begin_at', 'end_at', 'content']

    def __init__(self, user_id, tenant_id, rid, path, method, status_code,
                 begin_at, end_at, content=None):
        """Create a new audit log.
        :param user_id: User id who sends the request.
        :param tenant_id: Tenant id of the operated resource.
        :param rid: The code of the target resource.
        :param path: The path of the http request.
        :param method: The method of the http request.
        :param status_code: The status code of the response.
        :param start: The request received timestamp.
        :param end: The response sent timestamp.
        :param content: optional, the request body.
        """
        self.id = None
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.rid = rid
        self.path = path
        self.method = method
        self.status_code = status_code
        self.begin_at = begin_at
        self.end_at = end_at
        self.content = content


class Paginator(Model):
    """Paginator model class."""

    fields = ['total', 'count', 'size', 'current',
              'first', 'previous', 'next', 'last']

    def __init__(self, size=-1, marker=None, total=0, count=0,
                 first=None, previous=None, next=None, last=None):
        self.size = size
        "The records count per page, -1 means not limited"
        self.current = marker
        "The current page marker"
        self.total = total
        "The records total count"
        self.count = count
        "The total pages"
        self.first = first
        "The first page marker"
        self.previous = previous
        "The previous page marker"
        self.next = next
        "The next page marker"
        self.last = None
        "The last page marker"
