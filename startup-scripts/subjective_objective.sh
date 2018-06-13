#!/bin/bash
# creates + configures php web server

sudo yum install git-all
cd /home/ec2-user
git clone https://github.com/rob-dalton/subjective-objective-classifier.git
cd subjective-objective-classifier
make data
