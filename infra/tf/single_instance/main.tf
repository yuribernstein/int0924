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


variable "Purpose" {
  default = "Development"
}

resource "aws_instance" "backend" {
  ami           = "ami-05d38da78ce859165"
  instance_type = "t2.micro"
  count        = 2
    tags = {
    Purpose     = var.Purpose  
    Name        = "Backend"
    Owner       = "Yuri"
  }
}


resource "aws_instance" "frontend" {
  ami           = "ami-05d38da78ce859165"
  instance_type = "t2.micro"
  count        = 2
  tags = {
    Name        = "Frontend"
    Owner       = "Yuri"
  }
}


resource "aws_instance" "proxy" {
  ami           = "ami-05d38da78ce859165"
  instance_type = "t2.micro"
  count        = 1
  tags = {
    Name        = "Proxy"
    Owner       = "Yuri"
  }
}