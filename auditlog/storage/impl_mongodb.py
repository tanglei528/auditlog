import pymongo
import weakref

from auditlog.storage import base
from ceilometer.openstack.common import network_utils

from oslo.config import cfg



cfg.CONF.import_opt('auditlog_connection','auditlog.storage',group="database")

class MongoDBStorage(base.StorageEngine):
    """Engine to store data into mongodb."""

    def get_connection(self, conf):
	return Connection(conf)	 


class Connection(base.Connection):
    """MongoDB Connection."""

    def __init__(self, conf):
	
	self._pool = {}
	self.url = conf.database.auditlog_connection
	self.conn = self.connect(self.url)
	connection_options = pymongo.uri_parser.parse_uri(self.url)
	self.db = getattr(self.conn, connection_options['database'])

    def connect(self,url):

	connection_options = pymongo.uri_parser.parse_uri(url)
        del connection_options['database']
        del connection_options['username']
        del connection_options['password']
        del connection_options['collection']
        pool_key = tuple(connection_options)

        if pool_key in self._pool:
            client = self._pool.get(pool_key)()
            if client:
                return client
        splitted_url = network_utils.urlsplit(url)
        client = pymongo.MongoClient(url,safe=True)
        self._pool[pool_key] = weakref.ref(client)
        return client	  

    def upgrade(self):
        pass

    def create_auditlog(self, log):
	self.db.auditlog.insert(log)

    def get_auditlog_by_id(self, id):
	self.db.auditlog.find({"_id":"ObjectId("+id+")"})

    def get_auditlogs_paginated(self, q, paginator,
                                order_by=[], order_dir='asc'):
        pass
    def validate_query(self, q):
        pass
