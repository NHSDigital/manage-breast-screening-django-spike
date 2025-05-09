resource "azurerm_resource_group" "colin_spike" {
  name     = var.resource_group_name
  location = "uksouth"
}

resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  location            = azurerm_resource_group.colin_spike.location
  resource_group_name = azurerm_resource_group.colin_spike.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_log_analytics_workspace" "example" {
  name                = "acctest-01"
  location            = azurerm_resource_group.colin_spike.location
  resource_group_name = azurerm_resource_group.colin_spike.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}
