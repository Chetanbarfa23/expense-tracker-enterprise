// resource means we are creating somthing 

resource "aws_vpc" "expense_tracker_vpc" {

  cidr_block = "10.0.0.0/16"

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "Expense-Tracker-VPC"
  }
}