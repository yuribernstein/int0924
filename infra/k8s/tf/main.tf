terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

locals {
  instance_type = "t3.medium"
}

resource "aws_instance" "control_plane" {
  ami           = "ami-05d38da78ce859165"
  instance_type = local.instance_type
  count         = 1
  key_name      = "int_aws"
  tags = {
    Name     = "control_plane"
    k8s_role = "control_plane"
  }
    root_block_device {
    volume_size = 10  # Set the root disk size to 10GB
    volume_type = "gp2"  # You can specify the volume type as well, default is "gp2"
  }
}

resource "aws_instance" "worker" {
  ami           = "ami-05d38da78ce859165"
  instance_type = local.instance_type
  count         = 2
  key_name      = "int_aws"

  tags = {  
    Name     = "worker_${count.index + 1}"
    k8s_role = "worker"
  }
    root_block_device {
    volume_size = 10  # Set the root disk size to 10GB
    volume_type = "gp2"  # You can specify the volume type as well, default is "gp2"
  }
}

output "public_ips" {
  value = {
    control_pane = aws_instance.control_plane.*.public_ip
    workers       = { for i, worker in aws_instance.worker : "worker_${i + 1}" => worker.public_ip }
    
  }
}

output "private_ips" {
  value = {
    control_pane = aws_instance.control_plane.*.private_ip
    workers       = { for i, worker in aws_instance.worker : "worker_${i + 1}" => worker.private_ip }
  }
}