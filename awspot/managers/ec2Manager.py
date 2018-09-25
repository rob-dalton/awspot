import typing

from .base import Manager

class ec2Manager(Manager):
    """ Class for managing ec2 spot instances. """

    def _initialize_client(self, session):
        return session.client('ec2')

    def launch(self):
        from awspot.actions.ec2 import Launch
        action = Launch(self.client, self.parser, self.args)
        return action.execute()

    def terminate(self):
        from awspot.actions.ec2 import Terminate
        action = Terminate(self.client, self.parser, self.args)
        return action.execute()

    def list_active(self):
        from awspot.actions.ec2 import ListActive
        action = ListActive(self.client, self.parser, self.args)
        return action.execute()

    def ssh(self):
        from awspot.actions.ec2 import Ssh
        action = Ssh(self.client, self.parser, self.args)
        return action.execute()
    
    def execute(self, action: str):
        method = getattr(self, action)
        return method()