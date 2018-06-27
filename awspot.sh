#!/bin/bash

# exit function
die() {
    printf '%s\n' "$1" >&2
    exit 1
}

if [ -n "$1" ]; then
    case $1 in
        ec2)
            if [ $2 == 'ssh' ]; then
                $(python $AWSPOT_DIR/ec2.py "$@") 
            else
                python $AWSPOT_DIR/ec2.py "$@" 
            fi  
        ;;
        fleet) echo 'ERROR: Not implemented yet.';; 
        *) echo 'ERROR: Invalid command.';;
    esac
shift
else
    die 'ERROR: No resource type specified.'
fi
