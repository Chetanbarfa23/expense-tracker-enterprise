// But right now the VPC doesn’t have a path to the internet. now here is it 


resource "aws_internet_gateway" "expense_tracker_igw" {

  vpc_id = aws_vpc.expense_tracker_vpc.id

  tags = {
    Name = "Expense-Tracker-IGW"
  }
}