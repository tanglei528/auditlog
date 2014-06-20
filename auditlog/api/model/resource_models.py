import re


class Resource(object):
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
            "^(/v2/).*?(\/servers).*?(\/action)": {"2.2.7": "Update status"},
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
            {"2.2.18": "Rules for default security group"},
            "^(/v2/).*?(\/os-security-groups)": {"2.2.19": "Security groups"},
            "^(/v2/).*?(\/os-server-groups)": {"2.2.20": "Server groups"},
            "^(/v2/).*?(\/os-server-password)": {"2.2.21": "Server password"},
            "^(/v2/).*?(\/os-services)": {"2.2.22": "Manage services"},
            "^(/v2/).*?(\/os-volumes)": {"2.2.23": "Volume extension"},
            "^(/v2/).*?(\/os-snapshots)": {"2.2.24": "ossnapshots"},
            "^(/v2/).*?(\/servers).*?(\/os-volume_attachments)":
            {"2.2.25": "Volume attachments"},
            "^(/v2/).*?(\/servers).*?(?!action)": {"2.2.26": "Server"},
            "^(/v2/).*?(\/volumes)": {"3.2.1": "Volumes"},
            "^(/v2/).*?(\/snapshots)": {"3.2.2": "Snapshots"},
            "^(/v2/).*?(\/qos-specs)": {"3.2.3": "Quality of service(QoS)"},
            "^(/v2/).*?(\/os-quota-sets)": {"3.2.4": " Quota sets extension"},
            "^(/v2/).*?(\/backups)": {"3.2.5": "Backups extension"},
            "^(/v2/images)": {"4.2.1": "Images"},
            "^(/v2/images/).*?(\/tags)": {"4.2.2": "Image Tag"},
            "^(/v2/images/).*?(\/members)": {"4.2.3": "Image Member"},
            "^(/v1/)+[a-z0-9]": {"5.1.1": "Account"},
            "^(/v1/).*?(\/)[a-z0-9]": {"5.1.2": "Container"},
            "^(/v1/).*?(\/).*?(\/)": {"5.1.3": "Object"}
            }

    def __init__(self, rid="", rname=""):
        """Create a new audit log.
        """
        self.rid = rid
        self.rname = rname

    @classmethod
    def parse_url(cls, url):
        resource = None
        for key, value in cls.dict.items():
            resourceDict = re.findall(key, url, re.M)
            if resourceDict:
                for k, v in value.items():
                    resource = cls(rid=k, rname=v)
                break
        if resource is None:
            raise
        return resource

    @classmethod
    def get_resource_list(cls):
        list = []
        for _, v in cls.dict.items():
            for key, value in v.items():
                resource = Resource(rid=key, rname=value)
                list.append(resource)
        return list
