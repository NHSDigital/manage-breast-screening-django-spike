targetScope='subscription'

param enableSoftDelete bool
param envConfig string
param region string
param storageAccountRGName string
param storageAccountName string


var privateEndpointRGName = 'rg-hub-${envConfig}-uks-hub-private-endpoints'

resource storageAccountRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: storageAccountRGName
}
resource privateEndpointResourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateEndpointRGName
}


module terraformStateStorageAccount 'storage.bicep' = {
  scope: storageAccountRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: enableSoftDelete
  }
}

module storageAccountPrivateEndpoint 'privateEndpoint.bicep' = {
  scope: privateEndpointResourceGroup
  params: {
    envConfig: envConfig
    region: region
    storageName: storageAccountName
    storageAccountID: terraformStateStorageAccount.outputs.storageAccountID
  }
}
