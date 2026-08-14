resource "aws_instance" "expense_tracker_server" {

  ami           = var.ami_id
  instance_type = var.instance_type

  // this key_name is use to attach mac - ssh - ec2 
  key_name = "jenkins_key"

  subnet_id = aws_subnet.public_subnet.id

  vpc_security_group_ids = [
    aws_security_group.expense_tracker_sg.id
  ]

  tags = {
    Name = "Expense-Tracker-Terraform"
  }
}