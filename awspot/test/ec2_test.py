import boto3

from unittest import TestCase
from unittest.mock import Mock

from awspot.managers import ec2Manager

class TestEc2Manager(TestCase):
    # TODO: Find isolated way to mock boto3 calls. Moto does not provide enough
    #       functionality.

    MOCK_CLIENT_ATTRS = {
        'request_spot_instances.return_value': {
            'SpotInstanceRequests': [{'SpotInstanceRequestId': 'sir-fa789d54'}]
        },
        'describe_spot_instance_requests.return_value': {
            'SpotInstanceRequests': [{'InstanceId': 'i-0578da97c8ee56262'}]
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

        cls.manager = ec2Manager(mock_client)
        cls.launch_specs = './assets/ec2_launch_specs.json'
        cls.userdata = './assets/ec2_userdata.sh'
        cls.price = '0.070'

    def test_launch(self):
        result = self.manager.launch_instance('test',
                                              self.launch_specs,
                                              self.userdata,
                                              self.price)
        self.assertTrue(result)

    def test_terminate(self):
        result = self.manager.terminate('test')
        self.assertTrue(result)
