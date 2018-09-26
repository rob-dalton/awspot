# AWSpot 
AWSpot is a command line utility that makes managing Amazon AWS spot resources simple and intuitive. It's intended for one-off projects in which you want quick access to cheap, secure, easily deployed compute resources. With AWSpot, launching, accessing, and terminating EC2 spot instances can all be completed in seconds with short, single line commands.

Intuitive use is the priority. Thus, resources are referenced and managed by `name` instead of impossible to remember ID strings. Please note this is great for personal use and one-off applications, but may not be suitable for production code.

<br><br>*NOTE: The only available resource type is `ec2`. Spot fleet and EMR management are in progress.*

## Example Usage

Let's say I want to spin up a machine pre-loaded with Anaconda. Let's also assume I have a `launch_spec.json` file containing the basic settings for my machine (security groups, size, etc):
    {
      "ImageId": "ami-2ae0ab52",
      "KeyName": "ec2_default",
      "SecurityGroupIds": [ "sg-a60747df" ],
      "InstanceType": "t2.xlarge",
      "Placement": {
        "AvailabilityZone": "us-west-2a"
      },
      "IamInstanceProfile": {
          "Arn": "arn:aws:iam::028206436608:instance-profile/s3_access_only"
      }
    }


To launch an instance I need to do is run:<br>
    awspot ec2 launch -n myproject -s ./launch_spec.json -p "0.07"

To ssh into my machine, I simply run:
    awspot ec2 ssh -n myproject -i ~/.ssh/myawskey.pem -u ec2-user

Once I'm finished, I can terminate my instance with:
    awspot ec2 terminate -n myproject

It's as simple as that!

## Setup
1. Install and configure `aws_cli`: https://aws.amazon.com/cli/
2. Run `pip install awspot`

## Usage
Commands follow this pattern:
    awspot <resource_type> <action> <args>`

Below is a list of the available commands and their args.

### ec2
EC2 actions are accessed via `awspot ec2 <action> <args>`

<hr>
`launch`<br><br>
Launch an EC2 spot instance.
#### Args
  - `-s | --specifications`: Path to JSON file with launch specifications. (required)
  - `-u | --userdata`: Path to userdata script (runs on instance boot). (optional)
  - `-p | --price`: Max spot resource bid price. (required)
  - `-n | --name`: Spot resource name. (required)
<hr>
`terminate`<br><br>
Terminate an EC2 spot instance.
#### Args
`-n | --name`: Spot resource name. (required)
<hr>
`ssh`<br><br>
SSH into an active spot instance. Note that you can use the optional flag `--add_ssh_profile` to create an SSH profile for the resource. For example, creating a profile for the `myproject` instance in the example above would allow you to acess the instance with the command `ssh myproject`. You may then use the `--remove_ssh_profile` flag to remove the profile once the resource is terminated.
#### Args
- `-n | --name`: Spot resource name. (required)
- `-i | --identity_file`: .pem file for SSH authentication. (optional\*)
- `-u | --user`: user to login as. (optional\*)
- `--forward_agent`: Forward SSH agent from local machine. (optional)
- `--add_ssh_profile`: Create an SSH profile with the provided info.
- `--remove_ssh_profile`: Remove an SSH profile for an AWSpot resource with the provided name.
<hr>
`list_active`<br><br>
List active(running) EC2 spot instances.
<hr>

## Learn More
To learn more about AWS resource management, please refer to the resources below:
- [Launch specifications](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-request-examples.html)
- [User data scripts](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html#user-data-shell-scripts)
- [Max bid price](https://aws.amazon.com/ec2/spot/pricing/)
