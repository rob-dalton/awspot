import boto3
import unittest

from moto import mock_ec2

from managers import ec2Manager

class TestEc2Manager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = boto3.client('ec2')
        cls.manager = ec2Manager(cls.client)
        cls.launch_specs = 'specifications/default.json'
        cls.userdata = 'userdata_scripts/subjective_objective.sh'
        cls.price = '0.070'

    @mock_ec2
    def test_launch(self):
        result = self.manager.launch_instance('test',
                                              self.launch_specs,
                                              self.userdata,
                                              self.price)
        self.assertTrue(result)

    @mock_ec2
    def test_terminate(self):
        result = self.manager.terminate('test')
        self.assertTrue(result)
