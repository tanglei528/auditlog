from auditlog.storage import base


class MongoDBStorage(base.StorageEngine):
    """Engine to store data into mongodb."""

    def get_connection(self, conf):
        pass


class Connection(base.Connection):
    """MongoDB Connection."""

    def __init__(self, conf):
        pass

    def upgrade(self):
        pass

    def create_auditlog(self, log):
        pass

    def get_auditlog_by_id(self, id):
        pass

    def get_auditlogs_paginated(self, q, paginator,
                                order_by=[], order_dir='asc'):
        pass
