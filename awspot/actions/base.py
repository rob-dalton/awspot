class BaseAction(object):
    """ Base class for resource actions. """

    def __init__(self, client=None, parser=None, args=None):
        if (client is None) or (parser is None) or (args is None):
            raise ValueError('Action instance missing required arg.')

        self.client = client
        self.args = self._parse_args(parser, args)

    def _parse_args(self, parser, args):
        """ Method to add and parse action specific args """
        raise NotImplementedError

    def run(self, **kwargs):
        """ Method to run action """
        raise NotImplementedError