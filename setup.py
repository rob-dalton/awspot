from distutils.core import setup

setup(
    name='AWSpot',
    version='0.1.0',
    author='Rob Dalton',
    author_email='rob@robdalton.me',
    packages=['awspot', 'awspot.managers'],
    scripts=['bin/ec2.py'],
    url='http://pypi.python.org/pypi/AWSpot/',
    license='LICENSE',
    description='Utility for managing AWS spot resources.',
    long_description=open('README.md').read(),
    install_requires=[
        "boto3 >= 1.7.24"
    ],
)
