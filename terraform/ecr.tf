resource "aws_ecr_repository" "docker" {
  name                 = "admin-ecr"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_lifecycle_policy" "docker" {
  repository = aws_ecr_repository.docker.name

  policy = jsonencode({
    rules = [{
      rulePriority = 1
      description  = "Limit ECR to 10 images"
      action = {
        type = "expire"
      }
      selection = {
        tagStatus     = "any"
        countType     = "imageCountMoreThan"
        countNumber   = 10
      }
    }]
  })
}