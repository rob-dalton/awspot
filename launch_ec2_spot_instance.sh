#!/bin/bash

# exit function
die() {
    printf '%s\n' "$1" >&2
    exit 1
}

# loop through args
while :; do
    # pass each arg through case statement
    case $1 in 
        -s|--specification)
            if [ "$2" ]; then
                launch_spec_file=$2
            shift
            else
                die 'ERROR: "--specification" requires a non-empty option argument.'
            fi
        ;;
        -u|--userdata)
            if [ "$2" ]; then
                user_data_file=$2
            shift
            else
                die 'ERROR: "--userdata" requires a non-empty option argument.'
            fi
        ;;
        -p|--price)
            if [ "$2" ]; then
                spot_price=$2
            shift
            else
                die 'ERROR: "--price" requires a non-empty option argument.'
            fi
        ;;
        *) break
    esac
    shift
done

# convert UserData script file to base64, add to launch specifications
user_data="$(cat $user_data_file | base64)"
launch_specs="$(jq ".UserData=\"$user_data\"" $launch_spec_file)"

# setup request logfile name
log_file="instance-requests/$(date '+%y%m%d-%H%M%S').json"

# request spot instance
aws ec2 request-spot-instances --instance-count 1 \
                               --type "one-time" \
                               --spot-price "$spot_price" \
                               --launch-specification "$launch_specs" > $log_file

# get instance id, strip quotes from string
request_id="$(cat $log_file | jq '.SpotInstanceRequests[0] .SpotInstanceRequestId')"
request_state=$(aws ec2 describe-spot-instance-requests \
                --filters Name=spot-instance-request-id,Values=[$request_id])
instance_id=$(echo $request_state | jq '.SpotInstanceRequests[0] .InstanceId' | sed -e 's/^"//' -e 's/"$//')

# check if instance created every 5s
# TODO: Stop script if request is terminated
until [ -n $instance_id ]; do
    # TODO: Add wait spinner
    sleep 5s
done

# get instance DNS, strip quotes from string
instance_description=$(aws ec2 describe-instances \
                       --filters Name=instance-id,Values=[$instance_id])
instance_dns=$(echo $instance_description | jq '.Reservations[0] .Instances[0] .PublicDnsName' | sed -e 's/^"//' -e 's/"$//')

# add bash alias to ssh into instance 
# TODO: Add option to manage instances by name
echo "alias ssh_ec2_${instance_id}='ssh -i $AWS_PRIVATE_KEY ec2-user@${instance_dns}" >> ~/.aws_manager
