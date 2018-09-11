import argparse
import base64
import boto3
import json
import logging
import os
import time
import subprocess

from awspot.managers import ec2Manager

def parse_args():
    # TODO: Break ec2 commands into separate scripts w/separate args
    parser = argparse.ArgumentParser(description='Script to manage ec2 spot instances.')
    parser.add_argument('instance_type', type=str,
                        choices=['ec2'],
                        help='request_type (ec2 or spot fleet)')
    parser.add_argument('command', type=str,
                        choices=['launch', 'list_running', 'terminate',
                                 'ssh', 'jupytunnel'],
                        help='action type')
    parser.add_argument('-n', '--name', type=str,
                        help='name for instance')
    parser.add_argument('-s', '--specification', type=str,
                        help='path to specification JSON file')
    parser.add_argument('-d', '--userdata', type=str, default=None,
                        help='optional path to userdata shell script')
    parser.add_argument('-p', '--price', type=str,
                        help='max bid price for instance')
    parser.add_argument('-k', '--key_file', type=str,
                        help='path to .pem file')
    parser.add_argument('-u', '--user', type=str,
                        help='user to login as')
    parser.add_argument('-P', '--profile', type=str,
                        help='AWS profile to use', default='default')

    return parser.parse_args()


#################################################
# SCRIPT                                        #
#################################################
args = parse_args()

session = boto3.Session(profile_name=args.profile)
client = session.client('ec2')
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

    subprocess.run(["ssh", "-i", key_file,
                    f"{user_name}@{public_dns}"])

elif args.command == 'jupytunnel':
    instance = manager.find_instance_by_name(args.name)
    public_dns = instance['PublicDnsName']
    key_file = args.key_file
    user_name = args.user

    subprocess.run(["ssh", "-i", key_file,
                    "-N", "-L", "8000:localhost:8888",
                    f"{user_name}@{public_dns}"])

elif args.command == 'terminate':
    # TODO: Add console logging.
    manager.terminate(args.name)
