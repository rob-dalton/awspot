import datetime
import logging
import typing

from typing import List

from .base import Manager

class emrManager(Manager):
    """ Class for managing emr spot fleets. """

    def launch_cluster(self, name: str, launch_spec_file: str,
                        userdata_file: str, price: str):
        """ Launch emr cluster """
        raise NotImplementedError

    def list_active_clusters(self):
        """ List active instances of resource. """
        clusters = self._get_active_clusters()
        if not clusters:
            print("No active clusters.")
        else:
            output = "\nClusterId\t\tName\n\n"
            for cluster in clusters:
                name = cluster.get('Name')
                cluster_id = cluster.get('Id')
                output += f"{cluster_id}\t{name}\n"

        return output

    def find_cluster_by_name(self, name: str):
        """ Lookup cluster by name """
        # TODO: Handle case where multiple clusters have same name
        clusters = self._get_active_clusters()
        for cluster in clusters:
            if cluster['Name'] == name:
                return cluster

    def find_master_dns_by_name(self, name: str):
        """ Lookup cluster by name, return master public DNS """
        cluster = self.find_cluster_by_name(name)
        response = self.client.describe_cluster(ClusterId=cluster.get('Id'))
        dns = response['Cluster'].get('MasterPublicDnsName')

        return dns

    def terminate(self, name: str):
        """ Terminate resource by name. """
        raise NotImplementedError

    def _get_active_clusters(self)->List:
        """ Get list of active clusters created in last 30 days """
        cluster_states = ['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING']
        created_after = datetime.datetime.now() + datetime.timedelta(-30)

        response = self.client.list_clusters(ClusterStates=cluster_states,
                                             CreatedAfter=created_after)

        clusters = response.get('Clusters')

        return clusters
