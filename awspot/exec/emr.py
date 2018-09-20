import argparse
import boto3
import logging
import subprocess

from awspot.managers import emrManager

def parse_args():
    parser = argparse.ArgumentParser(description='Script to manage emr spot instance fleets.')
    parser.add_argument('instance_type', type=str,
                        choices=['emr'],
                        help='request_type')
    parser.add_argument('command', type=str,
                        choices=['launch', 'list_running', 'terminate',
                                 'ssh', 'jupytunnel'],
                        help='action type')
    parser.add_argument('-n', '--name', type=str,
                        help='name for instance')
    parser.add_argument('-c', '--configuration', type=str,
                        help='path to configuration JSON file')
    parser.add_argument('-b', '--bootstrap', type=str, default=None,
                        help='optional path to bootstrap shell script in s3')
    parser.add_argument('-p', '--price', type=str,
                        help='max bid price for instance(s)')
    parser.add_argument('-k', '--key_file', type=str,
                        help='path to .pem file')
    parser.add_argument('-u', '--user', type=str,
                        help='user to login as')
    parser.add_argument('-U', '--uniform', type=bool, default=True,
                        help='Use uniform pricing for cluster instances.')
    parser.add_argument('-P', '--profile', type=str,
                        help='AWS profile to use', default='default')
    parser.add_argument('--port', type=int,
                        help='host port to connect to', default=8888)
    parser.add_argument('-S', '--script', type=str,
                        help='path to aws cli launch script')
    parser.add_argument('--setup_profile', type=str, choices=['y', 'n'],
                        default='n', help='configure ssh profile')

    return parser.parse_args()

#################################################
# SCRIPT                                        #
#################################################
args = parse_args()

session = boto3.Session(profile_name=args.profile)
client = session.client('emr')
manager = emrManager(client)

if args.command == 'launch':
    # TODO: Expand functionality.
    response = manager.launch_cluster(launch_script=args.script,
                                      uniform=args.uniform, price=args.price,
                                      name=args.name)
    if 'ClusterId' in response:
        print(f"Cluster launched with ClusterId: {response['CluserId']}")
    else:
        print("ERROR: Cluster not launched.")

elif args.command == 'list_active_clusters':
    output = manager.list_active_clusters()
    print(output)

elif args.command == 'ssh':
    public_dns = manager.find_master_dns_by_name(args.name)
    key_file = args.key_file
    user_name = args.user

    if args.setup_profile == 'n':
        # if profile does not exist
        subprocess.run(["ssh", "-i", key_file,
                        f"{user_name}@{public_dns}"])
    else:
        manager.ssh_profile(name=args.name, user=user_name, action='add',
                            identity_file=key_file, public_dns=public_dns)

elif args.command == 'jupytunnel':
    public_dns = manager.find_master_dns_by_name(args.name)
    key_file = args.key_file
    user_name = args.user

    subprocess.run(["ssh", "-i", key_file,
                    "-N", "-L", f"8000:localhost:{args.port}",
                    f"{user_name}@{public_dns}"])

elif args.command == 'terminate':
    raise NotImplementedError
