#!/usr/bin/env python3

import boto3
import sys
import json

# AWS EC2 client
ec2 = boto3.client("ec2")

# Fetch instances by tag
def get_instances_by_tag(tag_key, tag_value):
    filters = [
        {
            "Name": f"tag:{tag_key}",
            "Values": [tag_value]
        },
        {
            "Name": "instance-state-name",
            "Values": ["running"]
        }
    ]

    response = ec2.describe_instances(Filters=filters)
    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            if "PublicIpAddress" in instance:
                instances.append(instance["PublicIpAddress"])

    return instances

# Generate the dynamic inventory in Ansible format
def generate_inventory(tag_key, tag_value):
    instances = get_instances_by_tag(tag_key, tag_value)

    inventory = {
        "all": {
            "hosts": instances,
            "vars": {}
        }
    }

    return inventory

# Handle --list or --host arguments from Ansible
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: aws_inventory.py [--list | --host <hostname>]")
        sys.exit(1)

    if sys.argv[1] == "--list":
        # Change the tag key and value as needed
        print(json.dumps(generate_inventory("Environment", "production"), indent=2))
    elif sys.argv[1] == "--host":
        # Ansible may request host-specific details; returning an empty dict for now
        print(json.dumps({}))
    else:
        print("Invalid argument")
        sys.exit(1)


# Run the script with --list to fetch the dynamic inventory
# modify the ansible.cfg file to use this script as the inventory source
# [defaults]
# inventory = ./dynamic_inventory.py
