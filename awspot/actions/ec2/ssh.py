import base64
import json
import logging
import os
import subprocess
import time
import typing

from typing import List

from .base import Ec2BaseAction

class Ssh(Ec2BaseAction):
    """ Class for managing ec2 spot instances. """

    def _parse_args(self, parser, args):
        parser.add_argument('-n', '--name', type=str, required=True,
                            help='name for instance')
        parser.add_argument('-i', '--identity_file', type=str, required=True,
                            help='path to .pem file')
        parser.add_argument('-u', '--user', type=str, required=True,
                            help='user to login as')
        parser.add_argument('--forward_agent', action='store_true',
                            help='forward SSH agent from local machine')
        parser.add_argument('--create_ssh_profile', action='store_true',
                            help='create profile for awspot ssh config file')
        parser.add_argument('--remove_ssh_profile', action='store_true',
                            help='remove profile for awspot ssh config file')

        return parser.parse_args()

    def create_ssh_profile(self, public_dns: str):
        """ Add profile to ssh config file. """
        config_path = os.path.expanduser("~") + "/.awspot/ssh_config"
        profile = f"\nHost {self.args.name}\n  HostName {public_dns}"
        profile += f"\n  User {self.args.user}\n  IdentityFile {self.args.identity_file}\n"
        if self.args.forward_agent:
            profile += f"\n ForwardAgent Yes\n"

        with open(config_path, 'a') as f:
            f.write(profile)

        print(f'\nProfile for {self.args.name} successfully created.\n')


    def remove_ssh_profile(self):
        config_path = os.path.expanduser("~") + "/.awspot/ssh_config"

        # get lines
        with open(config_path, 'r') as f:
            lines = f.readlines()

        # iterate over lines
        with open(config_path, 'w') as f:
            ignore = False
            for line in lines:
                # ignore lines from target Host til next host or EOF
                if f"Host {self.args.name}" in line:
                    ignore = True
                    continue

                if ignore:
                    if line[:5]=="Host ":
                        ignore = False
                    else:
                        continue
            
                f.write(line)

    def execute(self):
        # TODO: Automatically detect if profile exists for instance by name
        #       Use if so. Removes requirement for -i and -u args 
        instance = self._find_instance_by_name(self.args.name)
        public_dns = instance['PublicDnsName']

        if self.args.create_ssh_profile:
            self.create_ssh_profile(public_dns)
        elif self.args.remove_ssh_profile:
            self.remove_ssh_profile()
        else:
            subprocess.run(["ssh", "-i", self.args.identity_file,
                            f"{self.args.user}@{public_dns}"])