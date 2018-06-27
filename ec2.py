import argparse
import base64
import boto3
import json
import logging
import os
import time

from managers import ec2Manager

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
                        choices=['launch', 'list_running', 'terminate', 'ssh'],
                        help='action type')
    parser.add_argument('-n', '--name', type=str,
                        help='name for instance')
    parser.add_argument('-s', '--specification', type=str,
                        help='path to specification JSON file')
    parser.add_argument('-u', '--userdata', type=str,
                        help='optional path to user data shell script')
    parser.add_argument('-p', '--price', type=str,
                        help='max bid price for instance')

    return parser.parse_args()

if __name__ == "__main__":

    initialize_logging()
    args = parse_args()

    client = boto3.client('ec2')
    manager = ec2Manager(client)

    if args.command == 'launch':
        # TODO: Add console logging.
        manager.launch_instance(args.name,
                                args.specification,
                                args.userdata,
                                args.price)

    elif args.command == 'list_running':
        manager.list_running_instances()

    elif args.command == 'ssh':
        pem_key = os.environ['AWSPOT_KEY']
        user = os.environ['AWSPOT_USER']

        instance = manager.find_instance_by_name(args.name)
        dns = instance['PublicDnsName']

        print(f"ssh -i {pem_key} {user}@{dns}")

    elif args.command == 'terminate':
        # TODO: Add console logging.
        manager.terminate(args.name)
