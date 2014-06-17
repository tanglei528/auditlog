import datetime
import functools
import six
import wsme
from wsme import types as wtypes

from auditlog import utils

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


class Query(ViewModel):
    """Query filter."""

    # The data types supported by the query.
    _supported_types = ['integer', 'float', 'string', 'boolean']

    # Functions to convert the data field to the correct type.
    _type_converters = {'integer': int,
                        'float': float,
                        'boolean': functools.partial(
                            utils.bool_from_string, strict=True),
                        'string': six.text_type,
                        'datetime': utils.parse_isotime}

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
