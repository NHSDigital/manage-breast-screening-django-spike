targetScope='subscription'

param enableSoftDelete bool
param envConfig string
param region string
param storageAccountRGName string
param storageAccountName string

var hubMap = {
  dev: 'dev'
  int: 'dev'
  nft: 'dev'
  pre: 'prod'
  prd: 'prod'
}
var privateEndpointRGName = 'rg-hub-${envConfig}-uks-hub-private-endpoints'
var privateDNSZoneRGName = 'rg-hub-${hubMap[envConfig]}-uks-private-dns-zones'

resource storageAccountRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: storageAccountRGName
}
resource privateEndpointResourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateEndpointRGName
}
resource privateDNSZoneRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateDNSZoneRGName
}

module terraformStateStorageAccount 'storage.bicep' = {
  scope: storageAccountRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: enableSoftDelete
  }
}

output privateDNSZoneID string = privateDNSZone.outputs.privateDNSZoneID

module privateDNSZone 'dns.bicep' = {
  scope: privateDNSZoneRG
}

module storageAccountPrivateEndpoint 'privateEndpoint.bicep' = {
  scope: privateEndpointResourceGroup
  params: {
    hub: hubMap[envConfig]
    region: region
    storageName: storageAccountName
    storageAccountID: terraformStateStorageAccount.outputs.storageAccountID
    privateDNSZoneID: privateDNSZone.outputs.privateDNSZoneID
  }
}
