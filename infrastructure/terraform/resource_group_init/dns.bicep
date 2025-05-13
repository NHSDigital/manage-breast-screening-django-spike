var dnsZoneName = environment().suffixes.storage

// Retrieve the private DNS zone for storage accounts
resource privateDNSZone 'Microsoft.Network/privateDnsZones@2024-06-01' existing = {
  name: 'privatelink.blob.${dnsZoneName}'
}

output privateDNSZoneID string = privateDNSZone.id
