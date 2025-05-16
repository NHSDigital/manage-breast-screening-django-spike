param region string
param appShortName string
param envConfig string

resource mi 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  location: region
  name: 'mi-${appShortName}-${envConfig}-uks'
}
