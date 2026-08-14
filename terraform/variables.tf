variable "bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
}

variable "instance_type" {
  description = "EC2 Instance Type"
  type        = string
}

variable "ami_id" {
  description = "Ubuntu AMI ID"
  type        = string
}

variable "db_username" {
  description = "RDS database username"
  type        = string
  sensitive   = true
}
