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

# Get the default VPC in the region
data "aws_vpc" "default" {
  default = true
}

# Get a default subnet from that VPC
data "aws_subnet" "default" {
  vpc_id = data.aws_vpc.default.id
}

# Output the gathered data
output "vpc_id" {
  value = data.aws_vpc.default.id
}

output "subnet_id" {
  value = data.aws_subnet.default.id
}

# set variable environment
variable "environment" {
  default = "Development"
}

# Use that subnet in your instance
resource "aws_instance" "example" {
  ami           = "ami-05d38da78ce859165"
  instance_type = "t2.micro"
  count        = 1
  subnet_id     = data.aws_subnet.default.id
    tags = {
      Name        = "MyInstance"
      Environment = var.environment
      Owner       = "Yuri"
    }

    # Use local-exec to run Ansible after creating the instance
  provisioner "local-exec" {
    command = <<EOT
      ansible-playbook -i '${self.public_ip},' -u ubuntu --private-key /path/to/your/private/key playbook.yml
    EOT
  }
}

# Null resource to run Ansible
resource "null_resource" "ansible_provision" {
  provisioner "local-exec" {
    # command = "ansible-playbook -i '${aws_instance.example.public_ip},' playbook.yml"
    command = "ansible-playbook -i inventory_aws_ec2.yaml playbook.yml"
  }

  # Triggers Ansible when the instance changes
  triggers = {
    instance_id = aws_instance.example.id
  }
}