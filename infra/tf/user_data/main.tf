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

resource "aws_instance" "weather_app_instance" {
  ami           = var.ami
  instance_type = var.instance_type
  key_name      = var.key_name

  tags = {
    Name     = var.instance_name
    ExtraTag = local.extra_tag
  }

  user_data = <<-EOF
            #!/bin/bash
            sudo apt -y update && apt -y install docker.io
            sudo docker run -d -p 8080:8080 ${var.docker_image}
            EOF
}

output "instance_public_ip" {
  description = "The public IP address of the instance"
  value       = aws_instance.weather_app_instance.public_ip
}