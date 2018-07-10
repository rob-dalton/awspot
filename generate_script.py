# !/bin/bash python

import os
import argparse

awspot = """ \
#!/bin/bash

if [ -n "$1" ]; then
    case $1 in
        ec2)
            if [ $2 == 'ssh' ]; then
                $(python {0}/ec2.py "$@")
            else
                python {0}/ec2.py "$@"
            fi
        ;;
        fleet) echo 'ERROR: Not implemented yet.';;
        *) echo 'ERROR: Invalid command.';;
    esac
shift
else
    echo 'ERROR: No resource type specified.'
fi
"""

def parse_args():
    # get prefix arg
    parser = argparse.ArgumentParser(description='Script to manage ec2 spot instances.')
    parser.add_argument('--prefix', type=str, required=True,
                        help='Prefix to point to awspot brew install location.')

    return parser.parse_args()

if __name__ == "__main__":

    # setup args
    args = parse_args()

    # write bash script to file
    with open('./awspot', 'w') as f:
        f.write(awspot.format(args['prefix']))
