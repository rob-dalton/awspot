from .base import Ec2BaseAction

class ListActive(Ec2BaseAction):
    """ Action for listing active ec2 spot instances. """

    def _parse_args(self, parser, args):
        return None

    def execute(self):
        """ List active instances of resource. """
        instances = self._get_active_instances()
        if not instances:
            print("No running instances.")
        else:
            output = "\nInstanceId\t\tName\n\n"
            for instance in instances:
                name = self._get_instance_name(instance)
                instance_id = instance['InstanceId']
                output += f"{instance_id}\t{name}\n"

            print(output)