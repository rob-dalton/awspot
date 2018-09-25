import argparse
import json

from .base import Ec2BaseAction

class Terminate(Ec2BaseAction):
    """ Action for terminating ec2 spot instances. """

    def _parse_args(self, parser, args):
        # TODO: Add handling for case where multiple instances w/same name
        parser.add_argument('-n', '--name', type=str, required=True,
                            help='name for instance')
        return parser.parse_args(args)

    def execute(self):
        """ Terminate resource by name. """
        # TODO: Create fail-safe termination check.
        instance = self._find_instance_by_name(self.args.name)
        if instance:
            instance_id = instance['InstanceId']
            response = self.client.terminate_instances(InstanceIds=[instance_id])
            if response['TerminatingInstances'] and \
               response['TerminatingInstances'][0]['InstanceId'] == instance_id:
                print(f"\nInstance terminating:\n\n  Name: {self.args.name}\n  InstanceId: {instance_id}\n")
                return True

        return False