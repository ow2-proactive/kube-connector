import os

import tinydb

DIR = "./DB"
FILES = [
    "Clouds.json",
    "Tokens.json",
    "IPs.json",
    "Servers.json",
    "Security_Groups.json",
    "Cluster.json",
]
import logging


def create_database():
    create_dir()
    clouds = load_clouds()
    servers = load_servers()
    tokens = load_tokens()
    cluster = load_cluster()
    security_groups = load_security_groups()


def create_dir():
    isExist = os.path.exists(DIR)
    if not isExist:
        os.makedirs(DIR)
        logging.info("Created the DIR: " + DIR)


def load_clouds(file=DIR + "/Clouds.json"):
    db = tinydb.TinyDB(file)
    logging.info("Loaded clouds table")
    return db


def load_servers(file=DIR + "/Servers.json"):
    db = tinydb.TinyDB(file)
    logging.info("Loaded servers table")
    return db


def load_security_groups(file=DIR + "/Security_Groups.json"):
    db = tinydb.TinyDB(file)
    logging.info("Loaded servers table")
    return db


def load_tokens(file=DIR + "/Tokens.json"):
    db = tinydb.TinyDB(file)
    logging.info("Loaded tokens table")
    return db


def load_cluster(file=DIR + "/Cluster.json"):
    db = tinydb.TinyDB(file)
    logging.info("Loaded cluster table")
    return db


def add_cloud_item(cloud_item):
    cloud = load_clouds()
    cloud_table = cloud.table("Clouds")
    out = cloud_table.insert(cloud_item)
    return out


def add_server_item(server_item):
    servers = load_servers()
    servers_table = servers.table("Servers")
    out = servers_table.insert(server_item)
    return out


def add_ip_item(ip_item):
    cluster = load_cluster()
    ips_table = cluster.table("Ips")
    out = ips_table.insert(ip_item)
    return out


def add_cluster_sg_item(cluster_sg_item):
    cluster = load_cluster()
    SG_table = cluster.table("SG")
    out = SG_table.insert(cluster_sg_item)
    return out


def add_sg_item(sg_item):
    security_groups = load_security_groups()
    security_groups_table = security_groups.table("Security_Groups")
    out = security_groups_table.insert(sg_item)
    return out


def get_sg_ids():
    security_groups = load_security_groups()
    security_groups_table = security_groups.table("Security_Groups")
    out = [sg["id"] for sg in security_groups_table.all()]
    return out


def get_server_ids():
    servers = load_servers()
    servers_table = servers.table("Servers")
    out = [server["id"] for server in servers_table.all()]
    return out


def add_kubernetes_token(token):
    tokens = load_tokens()
    tokens_table = tokens.table("Tokens")
    out = tokens_table.insert({"token": token})
    return out


def get_security_group(sg_name):
    security_groups = load_security_groups()
    security_groups_table = security_groups.table("Security_Groups")
    query = tinydb.Query()
    return security_groups_table.search(query.name == sg_name)


def get_security_group_aws(sg_id, provider_name):
    security_groups = load_security_groups()
    security_groups_table = security_groups.table("Security_Groups")
    query = tinydb.Query()
    return security_groups_table.search(
        (query.id == sg_id)
        & (query.provider_name == provider_name)
        & (query.provider_type == "aws")
    )


def get_security_group_openstack(sg_name, provider_name):
    security_groups = load_security_groups()
    security_groups_table = security_groups.table("Security_Groups")
    query = tinydb.Query()
    return security_groups_table.search(
        (query.name == sg_name)
        & (query.provider_name == provider_name)
        & (query.provider_type == "openstack")
    )


def get_kubernetes_token(token_id):
    kubernetes_tokens = load_tokens()
    kubernetes_tokens_table = kubernetes_tokens.table("Tokens")
    return kubernetes_tokens_table.get(doc_id=token_id)


def clear_database():
    for file in FILES:
        to_be_deleted = f"{DIR}/{file}"
        if os.path.exists(to_be_deleted):
            os.remove(to_be_deleted)


def clear_sg_db():
    file = "Security_Groups.json"
    to_be_deleted = f"{DIR}/{file}"
    if os.path.exists(to_be_deleted):
        os.remove(to_be_deleted)
    load_security_groups()


def get_server_by_ip(ip):
    servers = load_servers()
    servers_table = servers.table("Servers")
    query = tinydb.Query()
    return servers_table.search(query.address == ip)


def add_ip_to_cluster(server):
    ip_item = {}
    ip_item["server_name"] = server["name"]
    ip_item["server_id"] = server["id"]
    ip_item["ip"] = server["address"]
    add_ip_item(ip_item)


def add_sg_to_cluster(server, sg):
    sg_item = {}
    sg_item["name"] = sg["name"]
    sg_item["id"] = sg["id"]
    sg_item["provider_name"] = sg["provider_name"]
    sg_item["provider_type"] = sg["provider_type"]
    sg_item["server"] = server["name"]
    add_cluster_sg_item(sg_item)


def get_server_sg(server):
    match server["provider_type"]:
        case "openstack":
            sg_name = server["security_groups"][0]
            sg_query = get_security_group_openstack(sg_name, server["provider_name"])
            if not sg_query:
                raise Exception('The security group with name "%s" was not found!' % sg_name)
                return
            elif len(sg_query) > 1:
                raise Exception(
                    'OpenStack chaos! two security groups with the same name "%s"' % sg_name
                )
                return
            else:
                sg = sg_query[0]
                return sg
        case "aws":
            sg_id = server["security_groups_ids"][0]
            sg_query = get_security_group_aws(sg_id, server["provider_name"])
            if not sg_query:
                raise Exception('The security group with id "%s" was not found!' % sg_id)
                return
            elif len(sg_query) > 1:
                raise Exception('AWS chaos! two security groups with the same id "%s"' % sg_id)
                return
            else:
                sg = sg_query[0]
                return sg


def get_cluster_ips():
    cluster = load_cluster()
    ips_table = cluster.table("Ips")
    ips = set()
    for ip in ips_table.all():
        ips.add(ip["ip"])
    return ips


def get_cluster_sgs():
    cluster = load_cluster()
    SG_table = cluster.table("SG")
    SGs = []
    for sg in SG_table.all():
        SGs.append(
            {
                "provider_name": sg["provider_name"],
                "provider_type": sg["provider_type"],
                "id": sg["id"],
            }
        )
    return SGs
