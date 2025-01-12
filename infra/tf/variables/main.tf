terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = var.region
}

locals {
  extra_tag = "additional-tag"
}

resource "aws_instance" "instance" {
  ami           = var.ami
  instance_type = var.instance_type

  tags = {
    Name     = var.instance_name
    ExtraTag = local.extra_tag
  }
}



# Two ways to declare variables
# 1. declare variables in the main.tf file, like in this example
# variable "instance_name" {}
# variable "ami" {}
# variable "instance_type" {}
# variable "region" {}
# 2. declare variables in a separate file variables.tf and assign values in a file terraform.tfvars

