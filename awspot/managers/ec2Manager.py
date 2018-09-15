import base64
import json
import logging
import os
import time
import typing

from typing import List

from .base import Manager

class ec2Manager(Manager):
    """ Class for managing ec2 spot instances. """

    def launch_instance(self, name: str, launch_spec_file: str,
                        userdata_file: str, price: str):
        """ Launch ec2 spot instance, store information by name. """
        # load launch specifications and base64 encoded userdata
        with open(launch_spec_file) as f:
            launch_spec = json.loads(f.read())
        if userdata_file is not None:
            with open(userdata_file) as f:
                userdata_str = f.read()
                userdata_bytes = base64.b64encode(bytes(userdata_str, 'utf-8'))
                userdata = userdata_bytes.decode('utf-8')
                launch_spec['UserData'] = userdata

        # request instance
        request = self.client.request_spot_instances(
            LaunchSpecification=launch_spec,
            SpotPrice=price
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
                       'Value': name}]
            )

            return True

        # handle failed fulfillment
        else:
            self.client.cancel_spot_instance_requests(
                SpotInstanceRequestIds=[request_id]
            )
            print(f"Spot instance request cancelled.\nReason: {request_status}\n")

            return False

    def list_running_instances(self):
        """ List active instances of resource. """
        instances = self._get_running_instances()
        if not instances:
            print("No running instances.")
        else:
            output = "\nInstanceId\t\tName\n\n"
            for instance in instances:
                name = self._get_instance_name(instance)
                instance_id = instance['InstanceId']
                output += f"{instance_id}\t{name}\n"

            print(output)

    def find_instance_by_name(self, name: str):
        """ Lookup resource by name """
        # TODO: Handle case where multiple instances have same name
        instances = self._get_running_instances()
        for instance in instances:
            if self._get_instance_name(instance) == name:
                return instance

    def terminate(self, name: str):
        """ Terminate resource by name. """
        # TODO: Create fail-safe termination check.
        instance = self.find_instance_by_name(name)
        if instance:
            instance_id = instance['InstanceId']
            response = self.client.terminate_instances(InstanceIds=[instance_id])
            if response['TerminatingInstances'] and \
               response['TerminatingInstances'][0]['InstanceId'] == instance_id:
                print(f"Instance terminating.\nName: {name}\nInstanceId: {instance_id}\n")
                return True

        return False

    def _get_instance_name(self, instance: List)->str:
        """ Get instance name from instance description """
        tags = instance['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']

    def _get_running_instances(self)->List:
        """ Get list of running instances """
        filters = {'instance-lifecycle': ['spot'],
                   'instance-state-name': ['running']}
        filters_list = [{'Name': k, 'Values': v} for k, v in filters.items()]

        response = self.client.describe_instances(Filters=filters_list)
        reservations = response.get('Reservations')
        instances = [i for r in reservations for i in r.get('Instances')]

        return instances
