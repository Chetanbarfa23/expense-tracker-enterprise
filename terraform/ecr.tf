resource "aws_ecr_repository" "expense_tracker" {

  name = "expense-tracker"

  image_scanning_configuration {
    scan_on_push = true
  }

  image_tag_mutability = "MUTABLE"

  tags = {
    Name = "Expense-Tracker-ECR"
  }
}