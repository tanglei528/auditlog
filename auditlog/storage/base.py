import abc
import six


class InvalidQuery(Exception):
    pass


@six.add_metaclass(abc.ABCMeta)
class StorageEngine(object):
    """Base class for storage engines."""

    @abc.abstractmethod
    def get_connection(self, conf):
        """Return a :class:`Connection` instance based on configuration."""
        raise NotImplementedError('get_connection method not implemented.')


@six.add_metaclass(abc.ABCMeta)
class Connection(object):
    """Base class for storage system connections."""

    @abc.abstractmethod
    def __init__(self, conf):
        """Constructor"""

    @abc.abstractmethod
    def upgrade(self):
        """Migrate the database schema to the current version."""

    @abc.abstractmethod
    def create_auditlog(self, log):
        """Create a new audit log instance."""

    @abc.abstractmethod
    def get_auditlog_by_id(self, id):
        """Query a audit log instance by id
        :param id: the audit log id to find.
        :return: A audit log, or None if not found by id.
        """

    @abc.abstractmethod
    def get_auditlogs_paginated(self, q, limit=-1, marker=None,
                                order_by=[]):
        """Return a ordered and paginated query result according query.
        :param q: the query filters.
        :param limit: the max records to return, -1 means not limited.
        :param marker: the start record id to fetch.
        :param order_by: a list of {field: direction} to sort by.
            Direction can be 'DESC', 'ASC'.
        :return: the tuple ([AuditLog], Paginator)
        """

    @abc.abstractmethod
    def validate_query(self, q):
        """Validate if the queries supported
        :param q: a list of queries.
        :return: None
        :raise: InvalidQuery exception when having invalid query
        """
