# =========================================================
# Public Subnet
# =========================================================

resource "aws_subnet" "public_subnet" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  cidr_block = "10.0.1.0/24"

  availability_zone = "ap-south-1a"

  map_public_ip_on_launch = true

  tags = {
    Name = "Expense-Tracker-Public-Subnet"
  }
}


# =========================================================
# Private Subnet 1
# =========================================================

resource "aws_subnet" "private_subnet" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  cidr_block = "10.0.2.0/24"

  availability_zone = "ap-south-1b"

  map_public_ip_on_launch = false

  tags = {
    Name = "Expense-Tracker-Private-Subnet-1"
  }
}


# =========================================================
# Private Subnet 2
# =========================================================

resource "aws_subnet" "private_subnet_2" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  cidr_block = "10.0.3.0/24"

  availability_zone = "ap-south-1c"

  map_public_ip_on_launch = false

  tags = {
    Name = "Expense-Tracker-Private-Subnet-2"
  }
}