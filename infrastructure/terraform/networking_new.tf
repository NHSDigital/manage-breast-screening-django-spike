module "main_vnet" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/vnet"

  name                                         = "vnet-${var.environment}-uks-manage"
  resource_group_name                          = azurerm_resource_group.main.name
  location                                     = local.region
  dns_servers                                  = [data.azurerm_private_dns_resolver_inbound_endpoint.this.ip_configurations[0].private_ip_address] # Use data source
  log_analytics_workspace_id                   = azurerm_log_analytics_workspace.example.id                                                        # TODO: recreate
  monitor_diagnostic_setting_vnet_enabled_logs = ["VMProtectionAlerts"]
  monitor_diagnostic_setting_vnet_metrics      = ["AllMetrics"]
  vnet_address_space                           = var.vnet_address_space

}

data "azurerm_private_dns_resolver" "this" {
  provider = azurerm.hub

  name                = "${var.hub}-uks-hub-private-dns-zone-resolver"
  resource_group_name = "rg-hub-${var.hub}-uks-private-dns-zones"
}

data "azurerm_private_dns_resolver_inbound_endpoint" "this" {
  provider = azurerm.hub

  name                    = "private-dns-resolver-inbound-endpoint"
  private_dns_resolver_id = data.azurerm_private_dns_resolver.this.id
}

data "azurerm_virtual_network" "hub" {
  provider = azurerm.hub

  name                = "VNET-${upper(var.hub)}-UKS-HUB"
  resource_group_name = local.hub_vnet_rg_name
}

module "peering_spoke_hub" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/vnet-peering"

  name                = "${module.main_vnet.name}-to-hub-peering"
  resource_group_name = azurerm_resource_group.main.name
  vnet_name           = module.main_vnet.name
  remote_vnet_id      = data.azurerm_virtual_network.hub.id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false

  use_remote_gateways = false
}

module "peering_hub_spoke" {
  providers = {
    azurerm = azurerm.hub
  }

  source = "../modules/dtos-devops-templates/infrastructure/modules/vnet-peering"

  name                = "hub-to-${module.main_vnet.name}-peering"
  resource_group_name = local.hub_vnet_rg_name
  vnet_name           = data.azurerm_virtual_network.hub.name
  remote_vnet_id      = module.main_vnet.id

  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = false

  use_remote_gateways = false
}


module "container_app_subnet" {
  source = "../modules/dtos-devops-templates/infrastructure/modules/subnet"

  name                                                           = "container_app_subnet"
  resource_group_name                                            = var.resource_group_name              # TODO: recreate
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
