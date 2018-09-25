import base64
import json
import logging
import os
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
        parser.add_argument('--forward_agent', type=bool, default=False,
                            'forward SSH agent from local machine')
        parser.add_argument('--create_ssh_profile', type=bool, default=False,
                            help='create profile for awspot ssh config file')

        return parser.parse_args()

    def create_ssh_profile(self, public_dns: str):
        """ Add profile to ssh config file. """
        config_path = os.path.expanduser("~") + "/.awspot/ssh_config"
        profile = f"\nHost {self.args.name}\n  HostName {public_dns}\n  User {self.args.user}"
        profile += f"\n  IdentityFile {self.args.identity_file}\n  ForwardAgent yes"

        with open(config_path, 'a') as f:
            f.write(profile)

    def remove_ssh_profile(self):
        #TODO: Add removal procedure. Move to terminate.
        pass

    def execute(self):
        # TODO: Automatically detect if profile exists for instance by name
        #       Use if so. Removes requirement for -i and -u args 
        instance = self._find_instance_by_name(self.args.name)
        public_dns = instance['PublicDnsName']

        if self.args.create_ssh_profile:
            self.create_ssh_profile(public_dns)
        else:
            subprocess.run(["ssh", "-i", self.args.identity_file,
                            f"{self.args.user}@{public_dns}"])