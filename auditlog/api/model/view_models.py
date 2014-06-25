import datetime
import functools
import six
import wsme
from wsme import types as wtypes

from auditlog.openstack.common import strutils
from auditlog.openstack.common import timeutils

HTTP_METHOD = ["GET", "PUT", "POST", "DELETE", "PATCH"]
operation_kind = wtypes.Enum(str, 'lt', 'le', 'eq', 'ne', 'ge', 'gt')


class ViewModel(wtypes.Base):
    """Base class for view models.
    The view model is the model used for the parameters of result of
    the controller methods.
    """

    @classmethod
    def from_model(cls, m):
        return cls(**(m.as_dict()))


class Resource(ViewModel):
    """The resources on which operations take place."""

    rid = wtypes.text
    "The id of the resource, a dot separated digital number string."

    name = wtypes.text
    "The name of the resource"


class AuditLog(ViewModel):
    """The audit log record."""

    id = wtypes.text
    "The id of this audit log."

    user_id = wtypes.text
    "The user this audit log was logged for."

    tenant_id = wtypes.text
    "The project this audit log was logged for."

    rid = wtypes.text
    "The :class:`Resource` this audit log was logged for."

    path = wtypes.text
    "The path of the request."

    method = wtypes.Enum(str, *HTTP_METHOD)
    "The method of the request."

    status_code = int
    "The status code of the response."

    begin_at = datetime.datetime
    "When the request was received."

    end_at = datetime.datetime
    "When the response was sent."

    content = wtypes.text
    "The content of the request."

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        fields = ['id', 'user_id', 'tenant_id', 'rid', 'path', 'method',
                  'status_code', 'begin_at', 'end_at', 'content']
        for f in fields:
            if not hasattr(other, f) or getattr(self, f) != getattr(other, f):
                return False

        return True


class Query(ViewModel):
    """Query filter."""

    # The data types supported by the query.
    _supported_types = ['integer', 'float', 'string', 'boolean']

    # Functions to convert the data field to the correct type.
    _type_converters = {'integer': int,
                        'float': float,
                        'boolean': functools.partial(
                            strutils.bool_from_string, strict=True),
                        'string': six.text_type,
                        'datetime': timeutils.parse_isotime}

    _op = None  # provide a default

    def get_op(self):
        return self._op or 'eq'

    def set_op(self, value):
        self._op = value

    field = wtypes.text
    "The name of the field to test"

    op = wsme.wsproperty(operation_kind, get_op, set_op)
    "The comparison operator. Defaults to 'eq'."

    value = wtypes.text
    "The value to compare against the stored data"

    type = wtypes.text
    "The data type of value to compare against the stored data"

    def __repr__(self):
        # for logging calls
        return '<Query %r %s %r %s>' % (self.field,
                                        self.op,
                                        self.value,
                                        self.type)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        if type(self) != type(other):
            return False
        if (self.field == other.field and self.op == other.op and
                self.value == other.value and self.type == other.type):
            return True
        return False


class Paginator(ViewModel):
    """The paginator view model."""

    total = int
    "Records total count"

    size = int
    "Records count per page"

    count = int
    "Total pages"

    current = wtypes.text
    "the marker of the current page"

    first = wtypes.text
    "the marker of the first page"

    previous = wtypes.text
    "the marker of the previous page"

    next = wtypes.text
    "the marker of the next page"

    last = wtypes.text
    "the marker of the last page"

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        fields = ['total', 'size', 'count', 'current', 'first',
                  'previous', 'next', 'last']
        for f in fields:
            if not hasattr(other, f) or getattr(self, f) != getattr(other, f):
                return False

        return True


class AuditLogPage(ViewModel):
    """The paginated audit log result class."""

    data = [AuditLog]
    "The audit log list in current page"

    paginator = Paginator
    "The paginator"
