# TODO: create KV with terraform
data "azurerm_key_vault" "app" {
  name                = "kv-colin-spike"
  resource_group_name = var.resource_group_name
}

data "azurerm_key_vault_secrets" "app" {
  key_vault_id = data.azurerm_key_vault.app.id
}
