# =========================================================
# RDS Subnet Group
# =========================================================

resource "aws_db_subnet_group" "expense_tracker_db_subnet_group" {

  name = "expense-tracker-db-subnet-group"

  subnet_ids = [
    aws_subnet.private_subnet.id,
    aws_subnet.private_subnet_2.id
  ]

  tags = {
    Name = "Expense-Tracker-DB-Subnet-Group"
  }
}


# =========================================================
# RDS Security Group
# =========================================================

resource "aws_security_group" "expense_tracker_rds_sg" {

  name        = "expense-tracker-rds-sg"
  description = "Security Group for Expense Tracker RDS"
  vpc_id      = aws_vpc.expense_tracker_vpc.id

  # MySQL
  ingress {
    description = "MySQL"

    from_port = 3306
    to_port   = 3306

    protocol = "tcp"

    # Temporary application access.
    # We will restrict this further when the EKS security group
    # is created.
    cidr_blocks = ["10.0.0.0/16"]
  }

  # Outbound traffic
  egress {
    from_port = 0
    to_port   = 0

    protocol = "-1"

    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "Expense-Tracker-RDS-SG"
  }
}

# =========================================================
# RDS MySQL Database
# =========================================================

resource "aws_db_instance" "expense_tracker_db" {

  identifier = "expense-tracker-db"

  engine         = "mysql"
  engine_version = "8.0"

  instance_class = "db.t3.micro"

  allocated_storage = 20
  storage_type      = "gp3"

  db_name  = "expense_tracker"
  username = var.db_username

  # AWS generates and manages the master password
  manage_master_user_password = true

  db_subnet_group_name = aws_db_subnet_group.expense_tracker_db_subnet_group.name

  vpc_security_group_ids = [
    aws_security_group.expense_tracker_rds_sg.id
  ]

  publicly_accessible = false

  backup_retention_period = 0

  skip_final_snapshot = true

  tags = {
    Name = "Expense-Tracker-RDS"
  }
}