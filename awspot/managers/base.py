import json
import typing

class Manager(object):
    """ Base class for spot resource managers."""

    def __init__(self, session, parser, args):
        self.client = self._initialize_client(session)
        self.parser = parser
        self.args = args

    def _initialize_client(self, session):
        """ Initialize client for resource """
        raise NotImplementedError

    def launch(self, **kwargs):
        """ Launch resource. """
        raise NotImplementedError

    def list_running(self, **kwargs):
        """ List running instances of resource. """
        raise NotImplementedError

    def terminate(self, **kwargs):
        """ Terminate resource by name. """
        raise NotImplementedError

    def execute(self):
        """ Execute appropriate action """
        raise NotImplementedError