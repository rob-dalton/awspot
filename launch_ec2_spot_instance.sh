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
printf "Making instance request...\n"
aws ec2 request-spot-instances --instance-count 1 \
                               --type "one-time" \
                               --spot-price "$spot_price" \
                               --launch-specification "$launch_specs" > $log_file

# get instance id, strip quotes from string
request_id=$(cat $log_file | jq '.SpotInstanceRequests[0] .SpotInstanceRequestId' | sed -e 's/^"//' -e 's/"$//')
printf "Request $request_id submitted.\n"

function get_request_state {
    aws ec2 describe-spot-instance-requests \
            --filters Name=spot-instance-request-id,Values=[$request_id]
}

function get_instance_id {
    echo $(get_request_state) | \
    jq '.SpotInstanceRequests[0] .InstanceId' | \
    sed -e 's/^"//' -e 's/"$//'
}

# check if instance created every 3s
# TODO: Stop script if request is terminated
spin="/-\|"
instance_id=$(get_instance_id)
while [ $instance_id == "null" ]; do
    # run spinner
    for i in `seq 1 30`; do
        j=$(( (j+1) %4 ))
        printf "\rWaiting for request to be fulfilled...${spin:$j:1}"
        sleep .1
    done
    instance_id=$(get_instance_id)
done
printf "\nRequest fulfilled.\nInstance id:\t$instance_id\n"

# get instance DNS, strip quotes from string
instance_description=$(aws ec2 describe-instances \
                       --filters Name=instance-id,Values=[$instance_id])
instance_dns=$(echo $instance_description | jq '.Reservations[0] .Instances[0] .PublicDnsName' | sed -e 's/^"//' -e 's/"$//')
printf "Instance DNS:\t$instance_dns\n"

# add bash alias to ssh into instance 
# TODO: Add option to manage instances by name
ssh_alias="alias ssh_ec2_${instance_id}='ssh -i $AWS_PRIVATE_KEY ec2-user@${instance_dns}'"
echo  $ssh_alias >> ~/.aws_manager
source ~/.bash_profile

printf "SSH into instance with command:\n$ssh_alias\n"
