import operator
import re


class Model(object):

    def as_dict(self):
        """Convert model to dict."""
        return dict([(k, getattr(self, k, None)) for k in self.fields])


class AuditLog(Model):
    """Audit Log model class."""

    fields = ['_id', 'user_id', 'tenant_id', 'rid', 'path',
              'method', 'status_code', 'begin_at', 'end_at', 'content']

    def __init__(self, _id, user_id, tenant_id, rid, path, method,
                 status_code, begin_at, end_at, content=None):
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
        self._id = _id
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
        self.last = last
        "The last page marker"


class ResourceId(str):
    """Resource Id class
    Resource Id is consist of multiple dot-separated digital strings. Every
    segment means a level in hiararchy.
    """

    def __init__(self, value):
        super(ResourceId, self).__init__(value)
        self.parts = [int(p) for p in value.split('.')]

    def __lt__(self, other):
        if id(self) == id(other) or str(self) == str(other):
            return False
        sl = len(self.parts)
        ol = len(other.parts)
        for i, s in enumerate(self.parts):
            if i < ol and s < other.parts[i]:
                return True
            if i >= ol or s > other.parts[i]:
                return False
        if sl < ol:
            return True
        return False

    def __gt__(self, other):
        return other.__lt__(self)

    def __eq__(self, other):
        if id(self) == id(other):
            return True
        sl = len(self.parts)
        ol = len(other.parts)
        if sl != ol:
            return False
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        if id(self) == id(other):
            return True
        ol = len(other.parts)
        for i, s in enumerate(self.parts):
            if i < ol and s < other.parts[i]:
                return True
            if i >= ol or s > other.parts[i]:
                return False
        return True

    def __ge__(self, other):
        return other.__le__(self)


class Resource(Model):
    """resource model class
    """

    dict = {"^(/v2.0/networks)": {"1.2.1": "NetWorks"},
            "^(/v2.0/subnets)": {"1.2.2": "Subnets"},
            "^(/v2.0/ports)": {"1.2.3": "Ports"},
            "^(/v2.0/routers)": {"1.2.4": "Router"},
            "^(/v2.0/floatingips)": {"1.2.5": "Floatingips"},
            "^(/v2/).*?(\/flavors)": {"2.2.1": "Flavors"},
            "^(/v2/).*?(\/flavors).*?(\/os-extra_specs)":
            {"2.2.2": "Flavor extra-specs"},
            "^(/v2/).*?(\/os-agents)": {"2.2.3": "Guest agents"},
            "^(/v2/).*?(\/os-aggregates)": {"2.2.4": "Host aggregates"},
            "^(/v2/).*?(\/os-certificates)": {"2.2.5": "Root certificates"},
            "^(/v2/).*?(\/os-cloudpipe)": {"2.2.6": "Cloudpipe"},
            "^(/v2/).*?(\/servers).*?(\/action)": {"2.2.7": "Update server"},
            "^(/v2/).*?(\/servers).*?(\/os-attach-interfaces)":
            {"2.2.8": "Attach interfaces"},
            "^(/v2/).*?(\/os-coverage)": {"2.2.9": "Coverage reports"},
            "^(/v2/).*?(\/os-fixed-ips)": {"2.2.10": "Fixed IP"},
            "^(/v2/).*?(\/os-floating-ipdns)":
            {"2.2.11": "Floating IP DNS records"},
            "^(/v2/).*?(\/os-floating-ips)": {"2.2.12": "Floating IPs"},
            "^(/v2/).*?(\/os-floating-ipsbulk)":
            {"2.2.13": "Floating IPs bulk"},
            "^(/v2/).*?(\/os-hosts)": {"2.2.14": "Hosts"},
            "^(/v2/).*?(\/os-keypairs)": {"2.2.15": "Keypairs"},
            "^(/v2/).*?(\/os-networks)": {"2.2.16": "OS-Networks"},
            "^(/v2/).*?(\/os-quota-sets)": {"2.2.17": "Quota sets"},
            "^(/v2/).*?(\/os-security-group-rules)":
            {"2.2.18": "Security group rules"},
            "^(/v2/).*?(\/os-security-groups)": {"2.2.19": "Security groups"},
            "^(/v2/).*?(\/os-server-groups)": {"2.2.20": "Server groups"},
            "^(/v2/).*?(\/os-server-password)": {"2.2.21": "Server password"},
            "^(/v2/).*?(\/os-services)": {"2.2.22": "Manage services"},
            "^(/v2/).*?(\/os-volumes)": {"2.2.23": "Volume extension"},
            "^(/v2/).*?(\/os-snapshots)": {"2.2.24": "ossnapshots"},
            "^(/v2/).*?(\/servers).*?(\/os-volume_attachments)":
            {"2.2.25": "Volume attachments"},
            "^(/v2/).*?(\/volumes)": {"3.2.1": "Volumes"},
            "^(/v2/).*?(\/snapshots)": {"3.2.2": "Snapshots"},
            "^(/v2/).*?(\/qos-specs)": {"3.2.3": "Quality of service(QoS)"},
            "^(/v2/).*?(\/backups)": {"3.2.4": "Backups extension"},
            "^(/v2/images)": {"4.2.1": "Images"},
            "^(/v2/images/).*?(\/tags)": {"4.2.2": "Image Tag"},
            "^(/v2/images/).*?(\/members)": {"4.2.3": "Image Member"}
            }

    def __init__(self, rid=None, name=""):
        """Create a new audit log.
        """
        self.rid = rid
        self.name = name

    def __repr__(self):
        return "<Resource '%s' '%s'>" % (str(self.rid), unicode(self.name))

    def as_dict(self):
        return {'rid': str(self.rid), 'name': unicode(self.name)}

    @classmethod
    def parse_url(cls, url):
        resource = None
        for key, value in cls.dict.items():
            resourceDict = re.findall(key, url, re.M)
            if resourceDict:
                for k, v in value.items():
                    resource = cls(rid=ResourceId(k), name=v)
                break
        if resource is None:
            raise Exception("Could not parse None", url)
        return resource

    @classmethod
    def get_resource_list(cls):
        list = []
        for _, v in cls.dict.items():
            for key, value in v.items():
                resource = Resource(rid=ResourceId(key), name=value)
                list.append(resource)
        list.sort(key=operator.attrgetter('rid'))
        return list
