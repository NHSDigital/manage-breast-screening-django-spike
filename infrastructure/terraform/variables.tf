variable "app_short_name" {
  description = "Application short name (6 characters)"
}

variable "environment" {
  description = "Application environment name"
}

variable "docker_image" {
  description = "Docker image full path including registry, repository and tag"
}

variable "resource_group_name" {
  description = "Name of the main resource group name. Not created by terraform."
}

locals {
  # resource_group_name = "colin-spike"
  region = "uksouth"
  resource_group_name_new = "rg-${var.app_short_name}-${var.environment}-uks"
}
