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

resource "azurerm_user_assigned_identity" "container_app_identity" {
  name                = "container-app-identity"
  location            = azurerm_resource_group.colin_spike.location
  resource_group_name = azurerm_resource_group.colin_spike.name
}

resource "azurerm_container_app" "manage-breast-screening-django" {
  # Limited to 32 characters
  name                         = "manage-breast-screening-django"
  container_app_environment_id = azurerm_container_app_environment.example.id
  resource_group_name          = azurerm_resource_group.colin_spike.name
  revision_mode                = "Single"

  identity {
    type = "UserAssigned"
    identity_ids = [ azurerm_user_assigned_identity.container_app_identity.id ]
  }

  # dynamic "secret" {
  #   for_each = data.azurerm_key_vault_secrets.app.secrets
  #   content {
  #     # KV secrets are uppercase and hyphen separated
  #     # app container secrets are lowercase and hyphen separated
  #     name = lower(secret.value.name)
  #     identity = azurerm_user_assigned_identity.container_app_identity.id
  #     key_vault_secret_id = secret.value.id
  #   }
  # }

  secret {
    name  = "secret-key"
    value = "abcd123"
  }

  template {
    container {
      name   = "manage-breast-screening-django-spike"
      image  = var.docker_image
      cpu    = 0.25
      memory = "0.5Gi"
      env {
        name = "ALLOWED_HOSTS"
        value = "manage-breast-screening-django.${azurerm_container_app_environment.example.default_domain}"
      }
      # dynamic "env" {
      #   for_each = data.azurerm_key_vault_secrets.app.secrets
      #   content {
      #     # Env vars are uppercase and underscore separated
      #     name = upper(replace(env.value.name, "-", "_"))
      #     # KV secrets are uppercase and hyphen separated
      #     # app container secrets are lowercase and hyphen separated
      #     secret_name = lower(env.value.name)
      #   }
      # }

      env {
        name = "SECRET_KEY"
        # TODO: read from key vault
        secret_name = "secret-key"
      }

    }
    min_replicas = 1
  }
  ingress {
    external_enabled           = true
    target_port                = 8000
    allow_insecure_connections = false
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

resource "azurerm_role_assignment" "key_vault_reader" {
  scope                = azurerm_resource_group.colin_spike.id
  role_definition_name = "Key Vault Reader"
  principal_id         = azurerm_user_assigned_identity.container_app_identity.principal_id
}
