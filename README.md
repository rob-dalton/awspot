# EC2 Spot Instance Launcher
Script to easily launch and configure Amazon AWS EC2 spot instances.

Running the script will request a spot instance with the specifications defined by the passed args. It will also create an alias to ssh into your newly created instance.

## Setup
- Install and configure `aws_cli`: https://aws.amazon.com/cli/
- Install `jq`: https://stedolan.github.io/jq/
- Set the environment variable `$AWS_PRIVATE_KEY` to your desired .pem key file.
  - You must provide a private key, as the script assumes you're using SSH to access your instance.
- Add the following to your `.bash_profile`: 
    ```
    # Added for aws manager
    if [ -f ~/.aws_manager ]; then
       source ~/.aws_manager
    fi
    ``` 

## Usage
```bash launch_ec2_spot_instance.sh -s <path-to-spec-file> -u <path-to-startup-script> -p <max-bid-price>``` 

Args:
- `-s | --specifications`: Path to JSON file with launch specifications.
- `-u | --userdata`: Path to user data bash script (runs on instance boot).
- `-p | --price`: Max spot instance bid price.

## Learn More
- Launch specifications: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html
- User data scripts: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- Max bid price: https://aws.amazon.com/ec2/spot/pricing/ 
