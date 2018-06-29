#!/bin/bash

# parse args
while :; do
    case $1 in
        -p|--path)
            if [ "$2" ]; then
                awspot_dir_path=$2
            shift
            else
                die 'ERROR: "-p | --path" requires a non-empty argument.'
            fi
        ;;
        *) break
    esac
    shift
done

# create awspot manager env file
user_path=~/
manager_file="$user_path.awspot_manager"
touch $manager_file
cat >> $manager_file <<EOL
# AWSPOT MANAGER ENV FILE
# env vars and aliases for awspot manager

# vars
export AWSPOT_MANAGER_FILE='$manager_file'
export AWSPOT_DIR='$awspot_dir_path'

# awspot alias
alias awspot='bash ${awspot_dir_path}awspot.sh'
EOL

# set .bash_profile to source .awspot_manager
cat >> $user_path.bash_profile <<EOL

# Added for awspot manager
if [ -f ~/.awspot_manager ]; then
   source ~/.awspot_manager
fi
EOL

# add vars to current session
source $manager_file
