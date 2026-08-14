resource "aws_route_table" "public_route_table" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  route {
    cidr_block = "0.0.0.0/0"

    gateway_id = aws_internet_gateway.expense_tracker_igw.id
  }

  tags = {
    Name = "Expense-Tracker-Public-RT"
  }
}

// connecting public subnet with route-table so route table tell public subnet to trasfer data throught internet gateway 
resource "aws_route_table_association" "public_subnet_association" {

  subnet_id = aws_subnet.public_subnet.id

  route_table_id = aws_route_table.public_route_table.id
}