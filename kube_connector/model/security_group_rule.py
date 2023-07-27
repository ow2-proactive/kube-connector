import logging


class SGR:
    def __init__(self, rule_item, sg_name, sg_id, provider_name, provider_type):
        self.parent_name = sg_name
        self.parent_id = sg_id
        self.provider = provider_name

        match provider_type:
            case "openstack":
                self.id = rule_item["id"]
                self.ethertype = rule_item["ethertype"]
                self.port_range_min = rule_item["port_range_min"]
                self.port_range_max = rule_item["port_range_max"]
                self.protocol = rule_item["protocol"]
                self.remote_ip_prefix = rule_item["remote_ip_prefix"]
                self.created_at = rule_item["created_at"]

            case "aws":
                if "FromPort" in rule_item.keys() and "ToPort" in rule_item.keys():
                    self.port_range_min = rule_item["FromPort"]
                    self.port_range_max = rule_item["ToPort"]
                    self.protocol = rule_item["IpProtocol"]
                else:
                    self.port_range_min = "N/A"
                    self.port_range_max = "N/A"
                    self.protocol = "icmp"

                self._aws_get_ip_prefix(rule_item["IpRanges"], rule_item["Ipv6Ranges"], rule_item)
                self.id = f"{self.parent_id}_{self.port_range_min}:{self.port_range_max}_{self.protocol}_{self.remote_ip_prefix}"

    def __str__(self) -> str:
        return f'{self.id} : Source "{self.remote_ip_prefix}" Range: "{self.port_range_min}:{self.port_range_max}" Protocol: "{self.protocol}"'

    def _aws_get_ip_prefix(self, ipv4_range, ipv6_range, rule_item):
        if ipv4_range:
            self.ethertype = "IPv4"
            self.remote_ip_prefix = ipv4_range[0]["CidrIp"]
        elif ipv6_range:
            self.ethertype = "IPv6"
            self.remote_ip_prefix = ipv4_range[0]["CidrIp"]
        else:
            logging.warn(
                "No port range was found a rule in the security group %s: \n %s"
                % (self.parent_id, rule_item)
            )
            self.ethertype = "N/A"
            self.remote_ip_prefix = "N/A"

    @staticmethod
    def from_dict():
        pass
