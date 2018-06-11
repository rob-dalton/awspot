# ec2-spot-instance-launcher
Script to easily launch and configure Amazon AWS EC2 spot instances.

Args:
- `-s | --specifications`: Path to launch specification JSON file.
- `-u | --userdata`: Path to user data bash script (runs on instance boot).
- `-p | --price`: Max spot instance bid price.

You can learn more about these items here:
- Launch specifications: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html
- User data scripts: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts
- Max bid price: https://aws.amazon.com/ec2/spot/pricing/ 
