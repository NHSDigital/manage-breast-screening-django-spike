workspace {

  model {
    user = person "Staff User" {
      description "A user of the system"
    }

    cis2 = softwareSystem "CIS2" {
      description "Central authentication system used to authenticate users"
      tags "External system"
    }

    hospitalGateway = softwareSystem "Gateway" {
      description "VM running within each hospital network"
    }

    breastScreeningSystem = softwareSystem "Breast Screening System" {

      manageScreening = container "Manage Breast Screening" "Web Application" "Allows users to manage breast screening appointments and records"
      azurePostgres = container "Azure Database for PostgreSQL" "PostgreSQL - Managed Service" "Stores screening data in a managed Azure Postgres instance"

      user -> cis2 "Authenticates via"
      cis2 -> manageScreening "Provides authentication token to"
      user -> manageScreening "Uses (once authenticated)"
      manageScreening -> azurePostgres "Reads from and writes to"
      manageScreening -> hospitalGateway "Communicates with"
    }
  }

  views {

    container breastScreeningSystem {
      include *
        autolayout lr
    }

    styles {
      element "External system" {
        background #AAAAAA
      }
    }

    theme default
  }
}
