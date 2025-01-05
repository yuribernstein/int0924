#!/bin/bash
PURPOSE=$1
echo "Purpose: $PURPOSE"

aws ec2 run-instances \
    --image-id ami-05d38da78ce859165  \
    --instance-type t2.micro \
    --key-name int_aws \
    --security-group-ids sg-02b3d29bdcd49a0cc \
    --subnet-id subnet-06d26c27601fa5b42 \
    --count 1 \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=yuri_$PURPOSE},{Key=Purpose,Value=$PURPOSE}]" \
--output json > instance-details.json


# aws ec2 describe-instances
# aws ec2 describe-instances --instance-ids <id>