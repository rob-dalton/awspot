import argparse
import base64
import boto3
import json
import logging
import os
import time

from managers import ec2Manager

def initialize_logging():
    # TODO: Get logging calls to print to console.
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
    parser.add_argument('-d', '--userdata', type=str,
                        help='optional path to userdata shell script')
    parser.add_argument('-p', '--price', type=str,
                        help='max bid price for instance')
    parser.add_argument('-k', '--key_file', type=str,
                        help='path to .pem file')
    parser.add_argument('-u', '--user', type=str,
                        help='user to login as')

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
        # TODO: Add key pair management
        instance = manager.find_instance_by_name(args.name)
        public_dns = instance['PublicDnsName']
        key_file = args.key_file
        user_name = args.user

        print(f"ssh -i {key_file} {user_name}@{public_dns}")

    elif args.command == 'terminate':
        # TODO: Add console logging.
        manager.terminate(args.name)
