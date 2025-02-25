module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.27"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = module.eks.cluster_name
  node_group_name = "eks-worker-nodes"
  node_role_arn   = module.eks.cluster_iam_role_arn
  subnet_ids      = module.vpc.private_subnets

  scaling_config {
    desired_size = 2
    max_size     = 2
    min_size     = 1
  }

  instance_types = [var.node_instance_type]

  remote_access {
    ec2_ssh_key = "my-key-pair"  # Ensure this key pair exists in AWS
  }

  depends_on = [module.eks]
}