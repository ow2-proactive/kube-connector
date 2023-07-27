import datetime
import logging


class Server:
    def __init__(self, server_dict, provider_name, provider_type):
        match provider_type:
            case "openstack":
                self.name = server_dict["name"]
                self.id = server_dict["id"]
                self.provider_type = provider_type
                self.provider_name = provider_name
                self.region = server_dict["location"]["region_name"]
                self.status = server_dict["status"]
                self.type = server_dict["flavor"]["id"]
                self.launched = server_dict["launched_at"]
                self._OS_get_ipv4(server_dict["addresses"])
                self._OS_get_security_groups(server_dict["security_groups"])

            case "aws":
                self.name = self._aws_get_name(server_dict)
                self.id = server_dict["InstanceId"]
                self.provider_type = provider_type
                self.provider_name = provider_name
                self.region = server_dict["Placement"]["AvailabilityZone"]
                self.status = server_dict["State"]["Name"]
                self.type = server_dict["InstanceType"]
                self.launched = str(server_dict["LaunchTime"])
                self._aws_get_ipv4(server_dict)
                self._aws_get_security_groups(server_dict["SecurityGroups"])

    def _OS_get_ipv4(self, addresses):
        for l in addresses.values():
            for address in l:
                if address["version"] == 4:
                    self.address = address["addr"]
                    return
        logging.warn(
            'No IPV4 address was found for the server "%s" with id "%s"' % (self.name, self.id)
        )
        self.address = "n/a"

    def _OS_get_security_groups(self, security_groups):
        # TODO add a method to automatically get the security group id
        temp_security_groups = []
        if not len(security_groups):
            logging.warn(
                'No security group was found for the server "%s" with id "%s"'
                % (self.name, self.id)
            )
        for security_group in security_groups:
            temp_security_groups.append(security_group["name"])
        self.security_groups = temp_security_groups

    def to_dict(self) -> dict:
        d = self.__dict__
        return d

    def _aws_get_name(self, server_dict):
        if "Tags" in server_dict.keys():
            for tag in server_dict["Tags"]:
                if "Key" in tag.keys() and "Value" in tag.keys() and tag["Key"] == "Name":
                    return tag["Value"]
        return f"aws_{server_dict['Placement']['AvailabilityZone']}_{server_dict['InstanceId']}"

    def _aws_get_ipv4(self, server_dict):
        if "PublicIpAddress" in server_dict.keys():
            self.address = server_dict["PublicIpAddress"]
        else:
            logging.warn(
                'No IPV4 address was found for the server "%s" with id "%s"' % (self.name, self.id)
            )
            self.address = "n/a"

    def _aws_get_security_groups(self, security_groups):
        temp_security_groups_names = []
        temp_security_groups_ids = []
        if not len(security_groups):
            logging.warn(
                'No security group was found for the server "%s" with id "%s"'
                % (self.name, self.id)
            )
        for security_group in security_groups:
            # TODO change this to tuples
            temp_security_groups_names.append(security_group["GroupName"])
            temp_security_groups_ids.append(security_group["GroupId"])
        self.security_groups = temp_security_groups_names
        self.security_groups_ids = temp_security_groups_ids
