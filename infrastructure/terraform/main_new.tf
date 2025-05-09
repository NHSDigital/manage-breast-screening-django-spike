resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name_new
  location = local.region
}

module "app-key-vault" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/key-vault"

  name                                             = "kv-${var.app_short_name}-${var.environment}"
  resource_group_name                              = azurerm_resource_group.main.name
  enable_rbac_authorization                        = true # TODO: make true by default?
  location                                         = local.region
  log_analytics_workspace_id                       = azurerm_log_analytics_workspace.example.id     # TODO: recreate
  monitor_diagnostic_setting_keyvault_enabled_logs = ["AuditEvent", "AzurePolicyEvaluationDetails"] # TODO: not required if not creating NSG
  monitor_diagnostic_setting_keyvault_metrics      = ["AllMetrics"]
  private_endpoint_properties = { # TODO: Some could be default?
    private_dns_zone_ids_keyvault        = [data.azurerm_private_dns_zone.key-vault.id]
    private_endpoint_enabled             = true
    private_endpoint_subnet_id           = module.container_app_subnet.id
    private_endpoint_resource_group_name = azurerm_resource_group.main.name
    private_service_connection_is_manual = false
  }
  soft_delete_retention = 7 # TODO: Allow disabling soft delete
}

module "container-app-environment" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/container-app-environment"

  name                       = "manage-breast-screening-${var.environment}"
  resource_group_name        = azurerm_resource_group.main.name                   # TODO: recreate
  log_analytics_workspace_id = azurerm_log_analytics_workspace.example.id # TODO: recreate
  vnet_integration_subnet_id = module.container_app_subnet.id
}

module "webapp" {
  source                       = "../modules/dtos-devops-templates/infrastructure/modules/container-app"
  name                         = "manage-breast-screening-web-${var.environment}"
  container_app_environment_id = module.container-app-environment.id
  resource_group_name          = azurerm_resource_group.main.name
  # app_key_vault_name           = "kv-colin-spike"
  app_key_vault_name           = module.app-key-vault.key_vault_name
  docker_image                 = var.docker_image
  environment_variables = {
    "ALLOWED_HOSTS" = "manage-breast-screening-web-${var.environment}.${module.container-app-environment.default_domain}"
  }
  is_web_app = true
  http_port  = 8000
}

# TODO: Create key vault
# TODO: Create log analytics workspace
# TODO: Configure app environment DNS suffix
