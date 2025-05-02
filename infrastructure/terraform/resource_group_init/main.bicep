targetScope='subscription'

param region string
param resourceGroupName string
param storageAccountName string
param enableSoftDelete bool

resource mainRG 'Microsoft.Resources/resourceGroups@2024-11-01' = {
  name: resourceGroupName
  location: region
}

module terraformStateStorageAccount 'storage.bicep' = {
  name: 'storageModule'
  scope: mainRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: enableSoftDelete
  }
}
