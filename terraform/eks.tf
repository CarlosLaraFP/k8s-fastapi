module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.0.0"

  cluster_name    = var.cluster_name
  cluster_version = "1.32"
  subnet_ids      = module.vpc.private_subnets
  vpc_id          = module.vpc.vpc_id
}

resource "aws_key_pair" "eks_key" {
  key_name   = "eks-key"  # Automatically creates a key pair
  public_key = file("~/.ssh/id_rsa.pub")  # Uses the local SSH public key
}

resource "aws_eks_node_group" "eks_nodes" {
  cluster_name    = module.eks.cluster_name
  node_group_name = "eks-worker-nodes"
  node_role_arn   = aws_iam_role.eks_node_role.arn
  subnet_ids      = module.vpc.private_subnets

  scaling_config {
    desired_size = 2
    max_size     = 2
    min_size     = 1
  }

  instance_types = [var.node_instance_type]

  remote_access {
    ec2_ssh_key = aws_key_pair.eks_key.key_name
  }

  depends_on = [module.eks]
}