terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "4.25.0"
    }
  }
  backend "azurerm" {
    container_name = "terraform-state"
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "colin_spike" {
  name     = local.resource_group_name
  location = "uksouth"
}

resource "azurerm_virtual_network" "example" {
  name                = "example-network"
  location            = azurerm_resource_group.colin_spike.location
  resource_group_name = azurerm_resource_group.colin_spike.name
  address_space       = ["10.0.0.0/16"]
}

resource "azurerm_subnet" "example" {
  name                 = "example-subnet"
  resource_group_name  = azurerm_resource_group.colin_spike.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.0.0/23"]
}

resource "azurerm_log_analytics_workspace" "example" {
  name                = "acctest-01"
  location            = azurerm_resource_group.colin_spike.location
  resource_group_name = azurerm_resource_group.colin_spike.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "example" {
  name                           = "my-environment"
  location                       = azurerm_resource_group.colin_spike.location
  resource_group_name            = azurerm_resource_group.colin_spike.name
  logs_destination               = "log-analytics"
  log_analytics_workspace_id     = azurerm_log_analytics_workspace.example.id
  infrastructure_subnet_id       = azurerm_subnet.example.id
  internal_load_balancer_enabled = true
}
