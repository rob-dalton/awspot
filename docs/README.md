# AWSpot 
AWSpot is a command line utility that makes managing Amazon AWS spot resources simple and intuitive.
*NOTE: The only available resource type is `ec2`. Spot fleet and EMR management are in progress.*

## Setup
1. Install and configure `aws_cli`: https://aws.amazon.com/cli/
2. Run `pip install awspot`

## Basic Usage
Commands follow this pattern: `awspot <resource_type> <command> <args>`.  For now, the only available `resource_type` is `ec2`. Below is a list of the available commands and their args:

`launch`
- `-s | --specifications`: Path to JSON file with launch specifications.
- `-u | --userdata`: Path to userdata script (runs on instance boot).
- `-p | --price`: Max spot resource bid price.
- `-n | --name`: Spot resource name.

`terminate`
- `-n | --name`: Spot resource name. 

`ssh`
- `-n | --name`: Spot resource name. 
- `-i | --identity_file`: .pem file for SSH authentication
- `-u | --user`: user to login as

`list_active`

## Learn More
- Launch specifications: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html
- User data scripts: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- Max bid price: https://aws.amazon.com/ec2/spot/pricing/ 
