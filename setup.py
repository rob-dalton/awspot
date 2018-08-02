#!/usr/bin/env python
from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='AWSpot',
    version='0.0.3',
    author='Rob Dalton',
    author_email='rob@robdalton.me',
    classifiers=(
        'Programming Language :: Python :: 3.6'
    ),
    packages=['awspot', 'awspot.managers'],
    scripts=['bin/awspot'],
    url='http://pypi.python.org/pypi/AWSpot/',
    license='LICENSE',
    description='Utility for managing AWS spot resources.',
    long_description=open('README.md').read(),
    install_requires=[
        "boto3 >= 1.7.24"
    ],
)
