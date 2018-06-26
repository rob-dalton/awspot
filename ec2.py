import argparse
import base64
import boto3
import json
import logging
import os
import time

def initialize_logging():
    logging.basicConfig(
        filename="output.log",
        level=logging.DEBUG,
        format="%(asctime)s:%(levelname)s:%(message)s"
    )

def parse_args():
    # NOTE: ec2 is only allowed instance_type
    parser = argparse.ArgumentParser(description='Script to manage ec2 spot instances.')
    parser.add_argument('instance_type', type=str,
                        choices=['ec2'],
                        help='request_type (ec2 or spot fleet)')
    parser.add_argument('command', type=str,
                        choices=['launch', 'list-active', 'terminate', 'ssh'],
                        help='action type')
    parser.add_argument('-n', '--name', type=str,
                        help='name for instance')
    parser.add_argument('-s', '--specification', type=str,
                        help='path to specification JSON file')
    parser.add_argument('-u', '--userdata', type=str,
                        help='optional path to user data shell script')
    parser.add_argument('-p', '--price', type=str,
                        help='path to specification JSON file')

    return parser.parse_args()

if __name__ == "__main__":

    initialize_logging()

    # setup vars
    args = parse_args()
    instance_name = args.name
    resources_file = os.environ['AWSPOT_RESOURCES_FILE']
    with open(resources_file, 'r') as f:
        resources = json.loads(f.read())

    # instantiate client
    client = boto3.client('ec2')

    # execute based on command type
    if args.command == 'launch':

        # load launch specifications and base64 encoded userdata
        with open(args.specification) as f:
            launch_spec = json.loads(f.read())
        with open(args.userdata) as f:
            user_data = base64.b64encode(f.read())

        launch_spec['UserData'] = user_data

        # request instance
        request = client.request_spot_instances(LaunchSpecification=launch_spec)
        request_id = request['SpotInstanceRequestId']
        logging.info(f"Request submitted with id: {request_id}")

        # get instance id
        instance_id = None
        while instance_id is None:
            request_state = client.describe_spot_instance_requests(SpotInstanceRequestIds=[request_id])
            instance_id = request_state['SpotInstanceRequests'].get('InstanceId')
            time.sleep('3s')

        logging.info(f"Request fulfilled. InstanceId: {instance_id}")

        # Add active instance to resources file.
        with open(resources_file) as f:
            resources['ec2']['active'][instance_name] = instance_id
            f.truncate()
            f.write(json.dumps(resources))


    elif args.command == 'list_active':
        pass

    elif args.command == 'terminate':
        pass


    # print output

    # list active spot instances

    # delete specified spot instance(s)

