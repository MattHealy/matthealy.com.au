title: Rotating AMI images in a Launch Configuration
timestamp: 2017-08-08 00:00:00
slug: rotate-ami-launch-config
tags: [amazon-web-services, aws, autoscaling, launch-configuration]
author: Matt Healy

Something awesome about using AWS is the ability to auto-scale your workloads. At the risk of over-simplifying it, you set up a Launch Configuration and an Autoscaling Group to which the Launch Configuration should apply. The Launch Configuration defines the EC2 instance type, security groups, base AMI image, and other attributes for your Autoscaling Group. Once this is all set up, you can have new machines spun up automatically based on the load experienced by your application.

Something not so awesome about using AWS is when you need to update the base AMI image for your launch configuration. For example, you may have installed a new required system package or code library to your application, and you need to ensure that all your instances now and in the future have this package installed. You create a new AMI image, but now what?

It turns out that for some reason AWS does not allow us to *update* Launch Configurations. We are only given the option of copying an existing launch configuration. So, we need to:

1. Copy the existing launch configuration "MyLC" to a new launch configuration "MyNewLC"
2. While creating the new launch configuration, update the base AMI image to the new one we've created.
3. Update our autoscaling group to use the new launch configuration.

This is fairly straightforward and easy enough... but I found that by the third time doing it I'd had enough and so I decided to write a script and automate the process.

(Hint: with AWS it helps to automate basically everything - any manual action is a possible human error waiting to happen)

<div class="text-center">                                                       
    <img src="/static/img/blog/all-the-things.png" width="600" />
</div>

Below is the script I ended up with. You can download this script from my Github and adapt to suit your use. You'll need to have the AWS CLI tools installed and be using a profile with the appropriate AWS permissions.

<a href="https://gist.github.com/MattHealy/9ddf69ba60ba614a5a836ee40731f8cc">https://gist.github.com/MattHealy/9ddf69ba60ba614a5a836ee40731f8cc</a>

    #!/bin/bash

    oldconfigname="$1"
    newconfigname="$2"
    ami="$3"

    KEYNAME="my_keypair_name"
    ASGROUP="my_autoscaling_group_name"
    SECURITYGROUP="sg-1234"
    INSTANCETYPE="t2.micro"

    if [ "$oldconfigname" = "" ]; then
        echo "Usage: ./rotate-ami-launch-config.sh <old_launch_config_name> <new_launch_config_name> <new_ami_id>"
        exit
    fi
    if [ "$newconfigname" = "" ]; then
       echo "Usage: ./rotate-ami-launch-config.sh <old_launch_config_name> <new_launch_config_name> <new_ami_id>"
       exit
    fi
    if [ "$ami" = "" ]; then
        echo "Usage: ./rotate-ami-launch-config.sh <old_launch_config_name> <new_launch_config_name> <new_ami_id>"
        exit
    fi

    echo "Creating new launch configuration"
    aws autoscaling create-launch-configuration \
        --launch-configuration-name "$newconfigname" \
        --key-name "$KEYNAME" \
        --image-id "$ami" \
        --instance-type "$INSTANCETYPE" \
        --security-groups "$SECURITYGROUP" \
        --block-device-mappings "[{\"DeviceName\": \"/dev/xvda\",\"Ebs\":{\"VolumeSize\":8,\"VolumeType\":\"gp2\",\"DeleteOnTermination\":true}}]"

    echo "Updating autoscaling group"
    aws autoscaling update-auto-scaling-group \
        --auto-scaling-group-name "$ASGROUP" \
        --launch-configuration-name "$newconfigname"

    echo "Deleting old launch configuration"
    aws autoscaling delete-launch-configuration --launch-configuration-name "$oldconfigname"

    echo "Finished"
