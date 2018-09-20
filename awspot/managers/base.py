import json
import typing

from os.path import expanduser

class Manager(object):
    """ Base class for spot resource managers."""

    def __init__(self, client):
        self.client = client

    def launch(self, **kwargs):
        """ Launch resource. """
        raise NotImplementedError

    def list_running(self, **kwargs):
        """ List running instances of resource. """
        raise NotImplementedError

    def terminate(self, **kwargs):
        """ Terminate resource by name. """
        raise NotImplementedError

    def ssh_profile(self, name: str, public_dns: str, user: str,
                     identity_file: str, action: str='add'):
        """ Add profile to ssh config file. """
        config_path = expanduser("~") + "/.awspot/ssh_config"
        profile = f"\nHost {name}\n  HostName {public_dns}\n  User {user}"
        profile += f"\n  IdentityFile {identity_file}\n  ForwardAgent yes"
        if action=='add':
            with open(config_path, 'a') as f:
                f.write(profile)
        elif action=='remove':
            #TODO: Add removal procedure
            pass
        else:
            raise ValueError(f'{action} is not a valid value for action.')
