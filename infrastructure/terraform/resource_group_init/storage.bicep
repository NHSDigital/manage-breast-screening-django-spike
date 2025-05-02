param storageLocation string
param storageName string
param enableSoftDelete bool

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
