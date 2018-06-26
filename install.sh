#!/bin/bash

# setup
user_path='/Users/robertdalton'
add_dir_path_var="export AWSPOT_DIR='$user_path/web-projects/spot-instance-launcher'"
add_resources_file_var="export AWSPOT_RESOURCES_FILE='$user_path/.awspot_resources'"
add_manager_file_var="export AWSPOT_MANAGER_FILE='$user_path/.awspot_manager'"

touch ~/.awspot_resources
touch ~/.awspot_manager
echo $add_resources_file_var >> ~/.awspot_manager
echo $add_manager_file_var >> ~/.awspot_manager

# source file with package env vars, aliases 
cat >> ~/.bash_profile <<EOL

# Added for awspot manager
if [ -f ~/.awspot_manager ]; then
   source ~/.awspot_manager
fi
EOL

# add vars to session
source ~/.awspot_manager

# run python setup file
python ./setup.py
