param region string
param appShortName string
param envConfig string

var miName = 'mi-${appShortName}-${envConfig}-uks'

resource mi 'Microsoft.ManagedIdentity/userAssignedIdentities@2024-11-30' = {
  location: region
  name: miName
}

output miPrincipalID string = mi.properties.principalId
output miName string = miName
