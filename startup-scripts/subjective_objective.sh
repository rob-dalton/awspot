#!/bin/bash

# install git
sudo yum -y install git-all

# install project dependencies
conda install -y numpy
conda install -y pandas

# clone project repo
cd /home/ec2-user
git clone https://github.com/rob-dalton/subjective-objective-classifier.git

# run project
cd subjective-objective-classifier
make data
