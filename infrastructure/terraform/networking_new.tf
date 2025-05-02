module "container_app_subnet" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "container_app_subnet"
  resource_group_name                                            = local.resource_group_name            # TODO: recreate
  vnet_name                                                      = azurerm_virtual_network.example.name # TODO: recreate
  address_prefixes                                               = ["10.0.4.0/23"]                      # TODO: could be default value?
  create_nsg                                                     = false
  location                                                       = "UK South"                                 # TODO: not required if not creating NSG
  monitor_diagnostic_setting_network_security_group_enabled_logs = []                                         # TODO: not required if not creating NSG
  log_analytics_workspace_id                                     = azurerm_log_analytics_workspace.example.id # TODO: recreate
  network_security_group_name                                    = "container_app_subnet"                     # TODO: create default name?
}

# TODO: Create VNET
# TODO: Peer VNET to hub
# TODO: Create private DNS zone for DNS suffix
