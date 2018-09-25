import boto3
import sys

from unittest import TestCase
from unittest.mock import Mock, patch

from awspot.etc import get_base_argparser
from awspot.managers import ec2Manager

class TestEc2Manager(TestCase):
    # TODO: Find isolated way to mock boto3 calls. Moto does not provide enough
    #       functionality.

    MOCK_CLIENT_ATTRS = {
        'request_spot_instances.return_value': {
            'SpotInstanceRequests': [{'SpotInstanceRequestId': 'sir-fa789d54'}]
        },
        'describe_spot_instance_requests.return_value': {
            'SpotInstanceRequests': [{'InstanceId': 'i-0578da97c8ee56262', 'Status': {'Code': 'fulfilled'}}]
        },
        'describe_instances.return_value': {
            'Reservations': [{
                    'Instances': [{
                            'InstanceId': 'i-0578da97c8ee56262',
                            'Tags': [{'Key': 'Name', 'Value': 'test'}]
                        }]
                }]
        },
        'terminate_instances.return_value': {
            'TerminatingInstances': [{'InstanceId': 'i-0578da97c8ee56262'}]
        }
    }

    @classmethod
    def setUpClass(cls):
        mock_client = Mock()
        mock_client.configure_mock(**cls.MOCK_CLIENT_ATTRS)

        mock_session = Mock()
        mock_session.configure_mock(**{'client.return_value': mock_client})

        cls.session = mock_session
        
    def test_launch(self):
        args = [
            'ec2', 'launch',
            '-n', 'test',
            '-s', './assets/ec2_launch_specs.json',
            '-u', './assets/ec2_userdata.sh',
            '-p', '0.070'
        ]
        manager = ec2Manager(self.session, get_base_argparser(), args)
        ret = manager.execute('launch')
        self.assertTrue(ret) 

    def test_terminate(self):
        args = [
            'ec2', 'terminate',
            '-n', 'test'
        ]
        manager = ec2Manager(self.session, get_base_argparser(), args)
        ret = manager.execute('terminate')
        self.assertTrue(ret)