#!/bin/bash

# convert UserData script file to base64, add to launch specifications
user_data="$(cat startup-scripts/subjective_objective.sh | base64)"
launch_specs="$(jq ".UserData=\"$user_data\"" specifications/ec2_spot_default.json)"

# setup request log
log_file="instance-requests/$(date '+%y%m%d-%H%M%S').json"

aws ec2 request-spot-instances --instance-count 1 \
                               --type "one-time" \
                               --spot-price "0.070" \
                               --launch-specification "$launch_specs" > $log_file

# get request id
request_id="$(cat $log_file | jq '.SpotInstanceRequests[0] .SpotInstanceRequestId')"

# check if instance created every 5s
# TODO: Stop script if request is terminated
request_state=$(aws ec2 describe-spot-instance-requests \
                --filters Name=spot-instance-request-id,Values=[$request_id])
instance_id=$(request_state | jq 'SpotInstanceRequests[0] .InstanceId')

until [ -n $instance_id ]; do
    # TODO: Add wait spinner
    sleep 5s
done

# get instance DNS
instance_description=$(aws ec2 describe-instances \
                       --filters Name=instance-id,Values=[$instance_id])
instance_dns=$($instance_description | jq 'Reservations[0] .Instances[0] .PublicDnsName')

# add DNS to bash
# TODO: Add option to manage instances by name
cat "alias ssh_ec2_$instance_id='ssh -i $AWS_PRIVATE_KEY ec2-user@$instance_dns" > ~/.aws_manager
