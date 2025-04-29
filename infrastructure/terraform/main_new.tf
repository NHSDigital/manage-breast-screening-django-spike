variable "environment" {
  description = "Application environment name"
}

module "container-app-environment" {
  source                     = "../modules/dtos-devops-templates/infrastructure/modules/container-app-environment"
  name                       = "manage-breast-screening-${var.environment}"
  resource_group_name        = local.resource_group_name                  # TODO: recreate
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id # TODO: recreate
  vnet_integration_subnet_id = azurerm_subnet.example.id                  # TODO: recreate
}
