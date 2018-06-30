# !/bin/bash python

import os

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

if __name__ == "__main__":

    with open('./awspot', 'w') as f:
        f.write(awspot.format(os.getcwd()))
