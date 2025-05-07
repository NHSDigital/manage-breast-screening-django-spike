param envConfig string
param region string
param storageName string
param storageAccountID string

var RGName = 'rg-hub-${envConfig}-uks-hub-networking'
var vnetName = 'VNET-${toUpper(envConfig)}-UKS-HUB'
var subnetName = 'SN-${toUpper(envConfig)}-UKS-HUB-pep'

// Retrieve the existing vnet resource group
resource vnetRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: RGName
  scope: subscription()
}

// Retrieve the existing vnet
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: vnetName
  scope: vnetRG
}

// Retrieve the existing Subnet within the vnet
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' existing = {
  parent: vnet
  name: subnetName
}

// Create the private endpoint for the storage account
resource privateEndpoint 'Microsoft.Network/privateEndpoints@2024-01-01' = {
  name: '${storageName}-pep'
  location: region
  properties: {
    subnet: {
      id: subnet.id
    }
    privateLinkServiceConnections: [
      {
        name: '${storageName}-connection'
        properties: {
          privateLinkServiceId: storageAccountID
          groupIds: [
            'blob'
          ]
        }
      }
    ]
  }
}
