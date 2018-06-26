import base64
import json
import logging
import os
import time
import typing

from .base import Manager

class ec2Manager(Manager):
    """ Class for managing ec2 spot instances. """

    def launch_instance(self, name: str, launch_spec_file: str,
                        userdata_file: str, price: str):
        """ Launch ec2 spot instance, store information by name. """
        # TODO: Add name to launch specifications as tag
        # load launch specifications and base64 encoded userdata
        with open(launch_spec_file) as f:
            launch_spec = json.loads(f.read())
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
            logging.error('Request submission failed.')
            return False
        else:
            logging.info(f"Request submitted with id: {request_id}")

        # get instance id
        instance_id = None
        while instance_id is None:
            request_state = self.client.describe_spot_instance_requests(
                SpotInstanceRequestIds=[request_id]
            )
            instance_id = request_state['SpotInstanceRequests'][0].get('InstanceId')
            time.sleep(3)

        logging.info(f"Request fulfilled. InstanceId: {instance_id}")

        # Add name tag to resource
        self.client.create_tags(
            Resources=[instance_id],
            Tags=[{'Key': 'Name',
                   'Value': name}]
        )

        return True

    def list_running_instances(self):
        """ List active instances of resource. """
        instances = self._get_running_instances()
        if not instances:
            print("No running instances.")
        else:
            output = "INSTANCES\n\nid\tname\n\n"
            for instance in instances:
                name = self._get_instance_name(instance)
                instance_id = instance['InstanceId']
                output += f"{instance_id}\t{name}\n"

            print(output)

    def terminate(self, **kwargs):
        """ Terminate resource by name. """
        raise NotImplementedError

    def _get_instance_name(self, instance):
        """ Get instance name from instance description """
        tags = instance['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']

    def _get_running_instances(self):
        """ Get list of running instances """
        filters = {'instance-lifecycle': ['spot'],
                   'instance-state-name': ['running']}
        filters_list = [{'Name': k, 'Values': v} for k, v in filters.items()]

        response = self.client.describe_instances(Filters=filters_list)
        reservations = response.get('Reservations')
        instances = [*[r.get('Instances') for r in reservations]]

        return instances
