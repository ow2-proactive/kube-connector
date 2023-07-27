import logging

from kube_connector.model.security_group_rule import SGR


class SG:
    def __init__(self, sg_item, provider_name, provider_type):
        self.provider_name = provider_name
        self.provider_type = provider_type

        match provider_type:
            case "openstack":
                self.name = sg_item["name"]
                self.id = sg_item["id"]
                self.description = sg_item["description"]
                self.rules = self._create_rules(
                    sg_item["security_group_rules"], provider_name, provider_type
                )
                self.created_at = sg_item["created_at"]
                self.revision_number = sg_item["revision_number"]

            case "aws":
                self.name = sg_item["GroupName"]
                self.id = sg_item["GroupId"]
                self.description = sg_item["Description"]
                self.rules = self._create_rules(
                    sg_item["IpPermissions"], provider_name, provider_type
                )
                self.vpc_id = sg_item["VpcId"]
                self.owner_id = sg_item["OwnerId"]

    def _create_rules(self, dict_rules, provider_name, provider_type):
        rules = []
        for dict_rule in dict_rules:
            rule = SGR(dict_rule, self.name, self.id, provider_name, provider_type)
            rules.append(rule)
        return rules

    def __str__(self) -> str:
        output = f'{self.name} : id "{self.id}" Provider: "{self.provider}": \n'
        if self.rules:
            output += f"\t rules: \n"
            for rule in self.rules:
                output += "\t\t" + rule.__str__() + "\n"
        return output

    def to_dict(self) -> dict:
        d = self.__dict__
        d["rules"] = [rule.__dict__ for rule in self.rules]
        return d

    @staticmethod
    def from_dict():
        pass
