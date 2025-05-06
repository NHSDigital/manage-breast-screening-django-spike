variable "docker_image" {
  description = "Docker image full path including registry, repository and tag"
}

variable "resource_group_name" {
  description = "Name of the main resource group name. Not created by terraform."
}

locals {
  # resource_group_name = "colin-spike"
}
