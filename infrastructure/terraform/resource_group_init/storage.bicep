param storageLocation string
param storageName string
param enableSoftDelete bool
param hubName string
param hubSubscriptionID string

var hubData = {
  dev: {
    vnet: 'VNET-DEV-UKS-HUB'
    vnetResourceGroup: 'rg-hub-dev-uks-hub-networking'
    pepSubnet: 'SN-DEV-UKS-HUB-pep'
  }
  prod: {
    vnet: 'VNET-PROD-UKS-HUB'
    vnetResourceGroup: 'rg-hub-prod-uks-hub-networking'
    pepSubnet: 'SN-PROD-UKS-HUB-pep'
  }
}

resource storageAccount 'Microsoft.Storage/storageAccounts@2024-01-01' = {
  name: storageName
  location: storageLocation
  sku: {
    name: 'Standard_RAGRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    // TODO
    // encryption: {
    //   requireInfrastructureEncryption: true
    // }
    minimumTlsVersion: 'TLS1_2'
    publicNetworkAccess: 'Disabled'
  }
}

resource vnetRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: hubData[hubName].vnetResourceGroup
  scope: subscription(hubSubscriptionID)
}

// Retrieve an existing Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2024-01-01' existing = {
  name: hubData[hubName].vnet
  scope: vnetRG
}

// Retrieve an existing Subnet within the Virtual Network
resource subnet 'Microsoft.Network/virtualNetworks/subnets@2024-01-01' existing = {
  parent: vnet
  name: hubData[hubName].pepSubnet
}

resource privateEndpoint 'Microsoft.Network/privateEndpoints@2024-01-01' = {
  name: '${storageName}-private-endpoint'
  location: storageLocation
  properties: {
    subnet: {
      id: subnet.id
    }
    privateLinkServiceConnections: [
      {
        name: '${storageName}-connection'
        properties: {
          privateLinkServiceId: storageAccount.id
          groupIds: [
            'blob'
          ]
        }
      }
    ]
  }
}

resource blobService 'Microsoft.Storage/storageAccounts/blobServices@2024-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    containerDeleteRetentionPolicy: {
      days: enableSoftDelete ? 15 : null
      enabled: enableSoftDelete
      allowPermanentDelete: enableSoftDelete
    }
    deleteRetentionPolicy: {
      days: enableSoftDelete ? 15 : null
      enabled: enableSoftDelete
      allowPermanentDelete: enableSoftDelete
    }
    isVersioningEnabled: true
  }
}

resource blobContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2024-01-01' = {
  parent: blobService
  name: 'terraform-state'
  properties: {
    publicAccess: 'None'
    defaultEncryptionScope: '$account-encryption-key'
    denyEncryptionScopeOverride: false
  }
}
