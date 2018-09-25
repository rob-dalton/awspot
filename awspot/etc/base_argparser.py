import argparse

def get_base_argparser():
    # setup default argument parser (will be passed down to scripts)
    parser = argparse.ArgumentParser(description='Script to manage AWS spot resources') 
    parser.add_argument('resource_type', type=str,
                        choices=['ec2', 'emr'],
                        help='resource type to manage')
    parser.add_argument('action', type=str,
                        choices=['launch', 'list_active', 'terminate', 'ssh'],
                        help='action type')
    parser.add_argument('--profile', type=str,
                        help='AWS profile to use', default='default')

    return parser
