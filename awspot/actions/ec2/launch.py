import argparse
import base64
import json
import logging
import os
import time
import typing

from typing import List

from .base import Ec2BaseAction

class Launch(Ec2BaseAction):
    """ Action class for launching ec2 spot instances. """

    def _parse_args(self, parser, args):
        parser.add_argument('-n', '--name', type=str, required=True,
                            help='name for instance')
        parser.add_argument('-s', '--specification', type=str, required=True,
                            help='path to specification JSON file')
        parser.add_argument('-p', '--price', type=str, required=True,
                            help='max bid price for instance')
        parser.add_argument('-u', '--userdata', type=str, default=None,
                            help='optional path to userdata shell script')

        return parser.parse_args(args)

    def execute(self):
        """ Launch ec2 spot instance, store information by name. """
        # load launch specifications and base64 encoded userdata
        with open(self.args.specification) as f:
            launch_spec = json.loads(f.read())
        if self.args.userdata is not None:
            with open(self.args.userdata) as f:
                userdata_str = f.read()
                userdata_bytes = base64.b64encode(bytes(userdata_str, 'utf-8'))
                userdata = userdata_bytes.decode('utf-8')
                launch_spec['UserData'] = userdata

        # request instance
        request = self.client.request_spot_instances(
            LaunchSpecification=launch_spec,
            SpotPrice=self.args.price
        )
        request_id = request['SpotInstanceRequests'][0].get('SpotInstanceRequestId')

        if request_id is None:
            print('Request submission failed.')
            return False
        else:
            print(f"\nSpot instance request submitted.\nSpotInstanceRequestId: {request_id}\n")

        # check request state every 1.5 seconds, get instance id when fulfilled
        holding = ['pending-evaluation','not-scheduled-yet',
                   'pending-fulfillment']
        request_status = 'pending-evaluation'
        while request_status in holding:
            request_state = self.client.describe_spot_instance_requests(
                SpotInstanceRequestIds=[request_id]
            )['SpotInstanceRequests'][0]
            request_status = request_state['Status'].get('Code')
            time.sleep(1.5)

        # handle successful fulfillment
        if request_status == 'fulfilled':
            instance_id = request_state.get('InstanceId')
            print(f"Spot instance request fulfilled.\nInstanceId: {instance_id}\n")
            # Add name tag to resource
            self.client.create_tags(
                Resources=[instance_id],
                Tags=[{'Key': 'Name',
                       'Value': self.args.name}]
            )

            return True

        # handle failed fulfillment
        else:
            self.client.cancel_spot_instance_requests(
                SpotInstanceRequestIds=[request_id]
            )
            print(f"Spot instance request cancelled.\nReason: {request_status}\n")

            return False