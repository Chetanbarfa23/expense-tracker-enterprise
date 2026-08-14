output "instance_id" {
  value = aws_instance.expense_tracker_server.id
}

output "public_ip" {
  value = aws_instance.expense_tracker_server.public_ip
}

output "public_dns" {
  value = aws_instance.expense_tracker_server.public_dns
}

output "ecr_repository_url" {

  value = aws_ecr_repository.expense_tracker.repository_url
}