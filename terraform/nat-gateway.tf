// aws_eip is a elastic ip is a public ip adress that remain same even if ec2 stop or restart 

resource "aws_eip" "nat_eip" {

  domain = "vpc"

  tags = {
    Name = "Expense-Tracker-NAT-EIP"
  }
}

resource "aws_nat_gateway" "expense_tracker_nat" {

  allocation_id = aws_eip.nat_eip.id

  // Put the NAT Gateway inside the Public Subnet.
  // Why public?
  // Because the NAT Gateway needs to communicate with the Internet Gateway.
  subnet_id = aws_subnet.public_subnet.id

  tags = {
    Name = "Expense-Tracker-NAT"
  }

  depends_on = [
    aws_internet_gateway.expense_tracker_igw
  ]
}


# Private Route Table
resource "aws_route_table" "private_route_table" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.expense_tracker_nat.id
  }

  tags = {
    Name = "Expense-Tracker-Private-RT"
  }
}


# Associate Private Subnet with Private Route Table
resource "aws_route_table_association" "private_subnet_association" {

  subnet_id = aws_subnet.private_subnet.id

  route_table_id = aws_route_table.private_route_table.id
}