variable "app_short_name" {
  description = "Application short name (6 characters)"
}

variable "environment" {
  description = "Application environment name"
}

variable "hub" {
  description = "Hub name (dev or prod)"
}

variable "docker_image" {
  description = "Docker image full path including registry, repository and tag"
}

variable "resource_group_name" {
  description = "Name of the main resource group name. Not created by terraform."
}

variable "hub_subscription_id" {
  description = "ID of the hub Azure subscription"
}

variable "vnet_address_space" {
  description = "VNET address space. Must be unique across the hub."
}
locals {
  # resource_group_name = "colin-spike"
  region = "uksouth"
  resource_group_name_new = "rg-${var.app_short_name}-${var.environment}-uks"
}
