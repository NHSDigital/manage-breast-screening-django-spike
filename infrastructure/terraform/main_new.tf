variable "environment" {
  description = "Application environment name"
}

module "container-app-environment" {
  source                     = "../modules/dtos-devops-templates/infrastructure/modules/container-app-environment"
  name                       = "manage-breast-screening-${var.environment}"
  resource_group_name        = local.resource_group_name                  # TODO: recreate
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id # TODO: recreate
  vnet_integration_subnet_id = module.container_app_subnet.id
}

module "webapp" {
  source                       = "../modules/dtos-devops-templates/infrastructure/modules/container-app"
  name                         = "manage-breast-screening-web-${var.environment}"
  container_app_environment_id = module.container-app-environment.id
  resource_group_name          = local.resource_group_name
  app_key_vault_name           = "kv-colin-spike"
  docker_image                 = var.docker_image
  environment_variables = {
    "ALLOWED_HOSTS" = "manage-breast-screening-django.${module.container-app-environment.default_domain}"
  }
  http_port = 8000
}
