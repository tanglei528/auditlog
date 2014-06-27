import pymongo
import uuid
import weakref

from oslo.config import cfg

from auditlog.api.model import models as mo
from auditlog.storage import base

cfg.CONF.import_opt('auditlog_connection', 'auditlog.storage',
                    group="database")


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
        self.colls = self.db.auditlog
        self.index = 0
        self.auditlog_list = []
        self.query_constraint_str = ""

    def connect(self, url):
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
        client = pymongo.MongoClient(url, safe=False)
        self._pool[pool_key] = weakref.ref(client)
        return client

    def upgrade(self):
        pass

    def create_auditlog(self, log):
        self.colls.insert(log)

    def get_auditlog_by_id(self, id):
        result = self.colls.find({"id": uuid.UUID(id)})
        return self._convert_results(result)[0]

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

        sort_comm = self._build_sort_instrution(order_by)
        query_cons = self._build_query_constraint(q)
        if order_by == []:
            results = self.colls.find(query_cons)
        else:
            results = self.colls.find(query_cons).sort(sort_comm)
        total = results.count()
        size = limit
        cursor = results.clone()

        if total == 0:
            return ([], None)
        if limit == -1:
            final = results
            auditlogs = self. _convert_results(final)
            return (auditlogs, None)
        else:
            if total > 0:
                if total <= size:
                    page_count = 1
                    first, previous, next, last = None, None, None, None
                else:
                    first = str(cursor.skip(size - 1)[0].get('id'))
                    last = str(cursor.skip(total - 1)[0].get('id'))
                    if total % size == 0:
                        page_count = total // size
                    else:
                        page_count = total // size + 1
                    if marker is None:
                        previous = None
                        next = str(cursor.skip(size - 1)[0].get('id'))
                        final = results.limit(limit)
                        paginator = mo.Paginator(limit, marker, total,
                                                 page_count, first, previous,
                                                 next, last)
                        auditlogs = self. _convert_results(final)
                        return (auditlogs, paginator)
                    else:
                        self._get_index_from_marker(results, marker)
                        idx_pre = self.index - size - 1
                        idx_next = self.index + size - 1
                        if idx_pre > 0:
                            previous = str(cursor.skip(idx_pre)[0].get('id'))
                        else:
                            previous = marker
                        if total < idx_next:
                            next = str(cursor.skip(total - 1)[0].get('id'))
                        else:
                            next = str(cursor.skip(idx_next)[0].get('id'))
                        begin_at = self._get_begintime(marker)
                        res = self.colls.find({"begin_at": {"$gt": begin_at}})
                        if self.index >= 1:
                            final = res[self.index: self.index + limit]
                        else:
                            final = res[:limit]
                        auditlogs = []
                        paginator = mo.Paginator(limit, marker, total,
                                                 page_count, first, previous,
                                                 next, last)
                        if final is not None:
                            auditlogs = self._convert_results(final)
                        return (auditlogs, paginator)

    def validate_query(self, q):
        pass

    def _build_sort_instrution(self, order_by=[]):
        result = []
        if order_by == []:
            return None
        for param in order_by:
            mid = param.split(':')
            if mid[1] == 'ASC':
                result.append((mid[0]), pymongo.ASCENDING)
            if mid[1] == 'DESC':
                    result.append((mid[0]), pymongo.DESCENDING)
        return result

    def _build_query_constraint(self, q=None):
        if q is None:
            return None
        for item in q:
            field = item.field
            op_list = {'lt': '$lt', 'le': '$le', 'eq': '$eq', 'ne': '$ne',
                       'ge': '$ge', 'gt': '$gt'}
            op = op_list.get(item.get_op())
            value = item.value
            self.query_constraint_str += {field: {op: value}} + ','

    def _get_index_from_marker(self, res, marker):
        for item in res:
            self.index += 1
            if str(item["id"]) == marker:
                break
            else:
                continue

    def _convert_results(self, results=None):
        log_list = []
        for item in results:
            id = str(item["id"])
            user_id = item["user_id"]
            tenant_id = item["tenant_id"]
            rid = item["rid"]
            path = item["path"]
            method = item["method"]
            status_code = item["status_code"]
            begin_at = item["begin_at"]
            end_at = item["end_at"]
            content = item["content"]
            log_list.append(mo.AuditLog(id, user_id, tenant_id, rid, path,
                                        method, status_code, begin_at,
                                        end_at, content))
        return log_list

    def _get_begintime(self, marker):
        id = uuid.UUID(marker)
        begin_at = self.colls.find({"id": id})[0]["begin_at"]
        return begin_at
