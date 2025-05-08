module "main_vnet" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/vnet"

  name                                                           = "vnet-${var.environment}-uks-manage"
  resource_group_name                                            = azurerm_resource_group.main.name
  location                                                       = local.region
  dns_servers                                                    = [data.azurerm_private_dns_resolver_inbound_endpoint.this.ip_configurations[0].private_ip_address] # Use data source
  log_analytics_workspace_id                                     = azurerm_log_analytics_workspace.example.id                                                                   # TODO: recreate
  monitor_diagnostic_setting_vnet_enabled_logs                   = []                                                                                                           # TODO: not required if not creating NSG
  monitor_diagnostic_setting_vnet_metrics                        = []
  vnet_address_space                                             = var.vnet_address_space

}

data "azurerm_private_dns_resolver" "this" {
  name                = "${hub}-uks-hub-private-dns-zone-resolver"
  resource_group_name = "rg-hub-${hub}-uks-private-dns-zones"
}

data "azurerm_private_dns_resolver_inbound_endpoint" "this" {
  name                    = "private-dns-resolver-inbound-endpoint"
  private_dns_resolver_id = data.azurerm_private_dns_resolver.this.id
}


module "container_app_subnet" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "container_app_subnet"
  resource_group_name                                            = var.resource_group_name            # TODO: recreate
  vnet_name                                                      = azurerm_virtual_network.example.name # TODO: recreate
  address_prefixes                                               = ["10.0.4.0/23"]                      # TODO: could be default value?
  create_nsg                                                     = false
  location                                                       = "UK South"                                 # TODO: not required if not creating NSG
  monitor_diagnostic_setting_network_security_group_enabled_logs = []                                         # TODO: not required if not creating NSG
  log_analytics_workspace_id                                     = azurerm_log_analytics_workspace.example.id # TODO: recreate
  network_security_group_name                                    = "container_app_subnet"                     # TODO: create default name?
}

data "azurerm_private_dns_zone" "key-vault" {
  provider = azurerm.hub

  name                = "privatelink.vaultcore.azure.net"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

# TODO: Create VNET
# TODO: Peer VNET to hub
# TODO: Create kv and private endpoint
