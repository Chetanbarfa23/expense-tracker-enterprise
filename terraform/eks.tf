# =========================================================
# EKS Cluster
# =========================================================

resource "aws_eks_cluster" "expense_tracker" {

  name = "expense-tracker-eks"

  role_arn = aws_iam_role.eks_cluster_role.arn

  vpc_config {

    subnet_ids = [
      aws_subnet.private_subnet.id,
      aws_subnet.private_subnet_2.id
    ]

    endpoint_public_access  = true
    endpoint_private_access = true
  }

  tags = {
    Name = "Expense-Tracker-EKS"
  }
}


# =========================================================
# EKS Managed Node Group
# =========================================================

resource "aws_eks_node_group" "expense_tracker" {

  cluster_name = aws_eks_cluster.expense_tracker.name

  node_group_name = "expense-tracker-nodes"

  node_role_arn = aws_iam_role.eks_node_role.arn

  subnet_ids = [
    aws_subnet.private_subnet.id,
    aws_subnet.private_subnet_2.id
  ]

  instance_types = [
    "t3.small"
  ]

  scaling_config {

    desired_size = 1
    min_size     = 1
    max_size     = 2
  }

  tags = {
    Name = "Expense-Tracker-EKS-Nodes"
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_ecr_policy,
    aws_iam_role_policy_attachment.eks_cni_policy
  ]
}
