from typing import List

from ..base import BaseAction

class Ec2BaseAction(BaseAction):
    """ Base class for ec2 actions. """

    def _find_instance_by_name(self, name: str):
        """ Lookup resource by name """
        # TODO: Handle case where multiple instances have same name
        instances = self._get_active_instances()
        for instance in instances:
            if self._get_instance_name(instance) == name:
                return instance

    def _get_instance_name(self, instance: List)->str:
        """ Get instance name from instance description """
        tags = instance['Tags']
        for tag in tags:
            if tag['Key'] == 'Name':
                return tag['Value']

    def _get_active_instances(self)->List:
        """ Get list of running instances """
        filters = {'instance-lifecycle': ['spot'],
                   'instance-state-name': ['running']}
        filters_list = [{'Name': k, 'Values': v} for k, v in filters.items()]

        response = self.client.describe_instances(Filters=filters_list)
        reservations = response.get('Reservations')
        instances = [i for r in reservations for i in r.get('Instances')]

        return instances

    def execute(self, **kwargs):
        """ Method to run action """
        raise NotImplementedError
