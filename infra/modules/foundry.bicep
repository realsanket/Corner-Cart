// A Microsoft Foundry resource (kind AIServices), one project, and one model deployment.
// Deliberately NO role assignment: a Bicep deployment does not give anyone Foundry User, so the first call
// from a service principal is a real 403 (lesson 13). The portal would have assigned it to you; Bicep does not.

@description('Globally unique name of the Foundry resource. Also its subdomain: https://<name>.openai.azure.com')
param accountName string

@description('Region. East US 2 offers the model as Global Standard.')
param location string = 'eastus2'

@description('Name of the project inside the resource.')
param projectName string = 'cornercart'

@description('The deployment name: what code passes as "model".')
param deploymentName string = 'gpt-5.4-mini'

@description('The catalogue model and version behind the deployment.')
param modelName string = 'gpt-5.4-mini'
param modelVersion string = '2026-03-17'

@description('Global Standard is pay-per-token. Capacity is in thousands of tokens per minute.')
param deploymentSku string = 'GlobalStandard'
param deploymentCapacity int = 50

@description('True = API keys are switched off, so Entra ID (a role) is the only way in.')
param disableLocalAuth bool = true

param tags object = {}

resource account 'Microsoft.CognitiveServices/accounts@2025-06-01' = {
  name: accountName
  location: location
  kind: 'AIServices'
  sku: { name: 'S0' }
  identity: { type: 'SystemAssigned' }
  tags: tags
  properties: {
    customSubDomainName: accountName
    allowProjectManagement: true // cannot be changed after creation
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: disableLocalAuth
  }
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-06-01' = {
  parent: account
  name: projectName
  location: location
  identity: { type: 'SystemAssigned' }
  properties: {}
}

resource deployment 'Microsoft.CognitiveServices/accounts/deployments@2025-06-01' = {
  parent: account
  name: deploymentName
  sku: {
    name: deploymentSku
    capacity: deploymentCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: modelName
      version: modelVersion
    }
  }
  dependsOn: [project] // one change at a time on the account
}

@description('The OpenAI-style base URL is this plus /openai/v1/ . Goes in FOUNDRY_ENDPOINT.')
output endpoint string = 'https://${accountName}.openai.azure.com'

@description('The project endpoint (for the Foundry SDK, used in AI-103).')
output projectEndpoint string = 'https://${accountName}.services.ai.azure.com/api/projects/${projectName}'

@description('Goes in FOUNDRY_DEPLOYMENT.')
output deploymentName string = deployment.name

output accountName string = account.name

@description('The scope for the role assignment: --scope <this>.')
output accountId string = account.id

output projectName string = project.name
