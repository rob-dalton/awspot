import json

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
