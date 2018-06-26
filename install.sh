#!/bin/bash

# set user path for install
user_path='/Users/robertdalton'
awspot_dir_path="$user_path/web-projects/spot-instance-launcher"
manager_file="$user_path/.awspot_manager"

# setup manager file and env var
touch $manager_file
echo "export AWSPOT_MANAGER_FILE='$manager_file'" >> $manager_file

# setup awspot dir env var
add_awspot_dir="export AWSPOT_DIR='$awspot_dir_path'"
echo $add_awspot_dir >> $manager_file

# setup awspot command alias
echo "alias awspot='bash $awspot_dir_path/awspot.sh'" >> $manager_file

# set .bash_profile to source manager file 
cat >> $user_path/.bash_profile <<EOL

# Added for awspot manager
if [ -f ~/.awspot_manager ]; then
   source ~/.awspot_manager
fi
EOL

# add vars to session
source $manager_file
