class AuditLog(object):
    """Audit Log model class."""

    def __init__(self, user_id, tenant_id, rid, method, status_code,
                 start, end, content=None):
        """Create a new audit log.
        :param user_id: User id who sends the request.
        :param tenant_id: Tenant id of the operated resource.
        :param rid: The code of the target resource.
        :param method: The method of the http request.
        :param status_code: The status code of the response.
        :param start: The request received timestamp.
        :param end: The response sent timestamp.
        :param content: optional, the request body.
        """
        self.user_id = user_id
        self.tenant_id = tenant_id
        self.rid = rid
        self.method = method
        self.status_code = status_code
        self.start = start
        self.end = end
        self.content = content
