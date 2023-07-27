import configparser
import os
import pprint

import boto3
from botocore.exceptions import ClientError

from kube_connector.model.security_group import SG
from kube_connector.model.server import Server

HOME_DIR = os.path.expanduser("~")


def create_aws_config_files(req):
    aws_dir = os.path.expanduser(f"{HOME_DIR}/.aws")
    os.makedirs(aws_dir, exist_ok=True)
    config_path = os.path.expanduser(f"{HOME_DIR}/.aws/config")
    credentials_path = os.path.expanduser(f"{HOME_DIR}/.aws/credentials")
    create_aws_config(req["region_name"], config_path)
    create_aws_credentials(req["aws_access_key_id"], req["aws_secret_access_key"], credentials_path)


def get_servers(providr_name):
    client = boto3.client("ec2")
    desired_states = ["running", "stopped"]
    response_dict = client.describe_instances(
        Filters=[{"Name": "instance-state-name", "Values": desired_states}]
    )
    servers = []
    for reservation in response_dict["Reservations"]:
        for instance in reservation["Instances"]:
            server = Server(instance, providr_name, "aws")
            servers.append(server)
    return servers


def get_security_groups(provider_name):
    security_groups = []
    ec2 = boto3.client("ec2")
    response = ec2.describe_security_groups()
    sg_items = response["SecurityGroups"]
    for sg_item in sg_items:
        security_group = SG(sg_item, provider_name, "aws")
        security_groups.append(security_group)
    return security_groups


def open_port(provider_name, sg_id, port):
    client = boto3.client("ec2")
    added_rule = client.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "FromPort": port["port_range_min"],
                "ToPort": port["port_range_max"],
                "IpProtocol": port["protocol"],
                "IpRanges": [{"CidrIp": port["ip"]}],  # Allow access from all IP addresses
            }
        ],
    )
    return added_rule


def open_ip(provider_name, sg_id, ip):
    port = {
        "direction": "ingress",
        "ip": f"{ip}/32",
        "protocol": "-1",
        "port_range_min": 0,
        "port_range_max": 65535,
    }
    added_rules = []
    added_rules.append(open_port(provider_name, sg_id, port))
    return added_rules


def create_aws_config(region, config_path):
    config = configparser.ConfigParser()
    config.add_section("default")
    config.set("default", "region", region)

    with open(config_path, "w") as configfile:
        config.write(configfile)


def create_aws_credentials(access_key, secret_key, credentials_path):
    config = configparser.ConfigParser()
    config.add_section("default")
    config.set("default", "aws_access_key_id", access_key)
    config.set("default", "aws_secret_access_key", secret_key)

    with open(credentials_path, "w") as configfile:
        config.write(configfile)
