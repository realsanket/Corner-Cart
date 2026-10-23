// Lab: your first model call. Deploys a Foundry resource + project + a Global Standard model deployment.
//
//   az group create -n rg-demo-cornercart-firstcall -l eastus2
//   az deployment group create -g rg-demo-cornercart-firstcall -f infra.bicep
//
// No role is assigned on purpose: the lab principal's first call is a 403.

targetScope = 'resourceGroup'

@description('Start of the resource name; a suffix from the resource group is added so the name is unique.')
param namePrefix string = 'ai-cornercart'

@description('Region.')
param location string = 'eastus2'

@description('The deployment name your code asks for.')
param deploymentName string = 'gpt-5.4-mini'

var suffix = take(uniqueString(resourceGroup().id), 5)

module foundry '../../infra/modules/foundry.bicep' = {
  name: 'foundry'
  params: {
    accountName: '${namePrefix}-${suffix}'
    location: location
    deploymentName: deploymentName
    modelName: 'gpt-5.4-mini'
    tags: { lab: 'ai-first-call-lab', app: 'cornercart' }
  }
}

output endpoint string = foundry.outputs.endpoint
output deploymentName string = foundry.outputs.deploymentName
output accountName string = foundry.outputs.accountName
output accountId string = foundry.outputs.accountId
