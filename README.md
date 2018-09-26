![AWSpot Logo](https://github.com/rob-dalton/rob-dalton.github.io/blob/master/images/awspot/awspot_logo_v1.png)

# AWS Spot Resource Manager
Command line utility to easily manage Amazon AWS spot resources.
*NOTE: Spot fleet management not implemented yet. EMR management partially implemented. The only fully available resource type is `ec2`.*

## Setup
1. Install and configure `aws_cli`: https://aws.amazon.com/cli/
2. Run `pip install awspot`

## Basic Usage
Commands follow this pattern: `awspot <resource_type> <command> <args>`. 

resource_type
- `ec2`
- `emr`

command
- `launch`
- `terminate`
- `list_active`
- `ssh`

args:
- `-s | --specifications`: Path to JSON file with launch specifications.
- `-u | --userdata`: Path to userdata script (runs on instance boot).
- `-p | --price`: Max spot resource bid price.
- `-n | --name`: Spot resource name.

## Learn More
- Launch specifications: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html
- User data scripts: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- Max bid price: https://aws.amazon.com/ec2/spot/pricing/ 
