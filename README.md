<img src="https://github.com/rob-dalton/rob-dalton.github.io/blob/master/images/awspot/awspot_logo_v1.png" width="320" alt="awspot-logo">

# AWS Spot Resource Manager
Command line utility to easily manage Amazon AWS spot resources.
*NOTE: The only available resource type is `ec2`. Spot fleet and EMR management are in progress.*

## Setup
1. Install and configure `aws_cli`: https://aws.amazon.com/cli/
2. Run `pip install awspot`

## Usage
Commands follow this pattern: `awspot <resource_type> <command> <args>`. For a list of the available commands and their args, please refer to [the project docs](https://rob-dalton.github.io/awspot). 

## Learn More
- Launch specifications: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html
- User data scripts: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- Max bid price: https://aws.amazon.com/ec2/spot/pricing/ 
