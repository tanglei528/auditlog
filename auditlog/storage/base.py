import abc
import six


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
        """Query a audit log instance by id."""

    @abc.abstractmethod
    def get_auditlogs_paginated(self, q, paginator,
                                order_by=[], order_dir='asc'):
        """Return a ordered and paginated query result according query."""
