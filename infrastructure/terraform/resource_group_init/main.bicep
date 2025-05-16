targetScope='subscription'

param enableSoftDelete bool
param envConfig string
param region string
param storageAccountRGName string
param storageAccountName string
param appShortName string

var hubMap = {
  dev: 'dev'
  int: 'dev'
  nft: 'dev'
  pre: 'prod'
  prd: 'prod'
}
var privateEndpointRGName = 'rg-hub-${envConfig}-uks-hub-private-endpoints'
var privateDNSZoneRGName = 'rg-hub-${hubMap[envConfig]}-uks-private-dns-zones'
var managedIdentityRGName = 'rg-mi-${envConfig}-uks'


// Retrieve existing terraform state resource group
resource storageAccountRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: storageAccountRGName
}
// Retrieve existing private endpoint resource group
resource privateEndpointResourceGroup 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateEndpointRGName
}
// Retrieve existing private DNS zone resource group
resource privateDNSZoneRG 'Microsoft.Resources/resourceGroups@2024-11-01' existing = {
  name: privateDNSZoneRGName
}

// Create the storage account, blob service and container
module terraformStateStorageAccount 'storage.bicep' = {
  scope: storageAccountRG
  params: {
    storageLocation: region
    storageName: storageAccountName
    enableSoftDelete: enableSoftDelete
  }
}

// Retrieve private DNS zone
module privateDNSZone 'dns.bicep' = {
  scope: privateDNSZoneRG
}

// Create private endpoint and register DNS
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

// Create the managed identity for CD
module managedIdentiy 'managedIdentity.bicep' {
  scope: managedIdentityRGName
  params: {
    region: region
    appShortName: appShortName
    envConfig: envConfig
  }
}
