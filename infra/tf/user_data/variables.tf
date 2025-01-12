variable "instance_name" {
  description = "Name of the instance"
  type        = string
}

variable "ami" {
  description = "AMI ID for the instance"
  type        = string
}

variable "instance_type" {
  description = "Instance type"
  type        = string
}

variable "region" {
  description = "AWS region"
  type        = string
}

variable "docker_image" {
  description = "Docker image to run"
  type        = string
}

variable "key_name" {
  description = "Name of the key pair"
  type        = string
}