import boto3

from unittest import TestCase
from unittest.mock import Mock

from awspot.managers import emrManager
from awspot.test import read_response

class TestEmrManager(TestCase):
    MOCK_CLIENT_ATTRS = {
        'list_clusters.return_value': {
            'Clusters': [{'Id': 'j-323SIFSG3JICT',
                          'Name': 'awspot-emr-test'}]
        },
        'describe_cluster.return_value':
        read_response('./assets/responses/emr_describe_cluster_response.json')
    }

    @classmethod
    def setUpClass(cls):
        mock_client = Mock()
        mock_client.configure_mock(**cls.MOCK_CLIENT_ATTRS)

        cls.manager = emrManager(mock_client)
        cls.price = '0.10'

    def test_launch(self):
        # TODO: Implement.
        pass

    def test_terminate(self):
        # TODO: Implement.
        pass

    def test_list_running(self):
        expected = "\nClusterId\t\tName\n\nj-323SIFSG3JICT\tawspot-emr-test\n"
        result = self.manager.list_active_clusters()

        self.assertEqual(expected, result)

    def test_find_dns_by_name(self):
        expected = 'ec2-34-211-56-169.us-west-2.compute.amazonaws.com'
        result = self.manager.find_master_dns_by_name('awspot-emr-test')

        self.assertEqual(expected, result)
