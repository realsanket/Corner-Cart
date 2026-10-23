# Lesson 13: Your first model call, 403 then 200

**Goal.** Authenticated is not authorized, seen live. `ask_the_shop.py` signs in and gets a **403**. You assign one
role, **Foundry User**, on the Foundry resource, and the same script returns **200** and the first "Ask the shop"
sentence. The call is keyless: no API key anywhere.

**Prerequisites.**
[`ai-foundry-model-deploy-lab`](../ai-foundry-model-deploy-lab/) (what a deployment is),
[`id-default-azure-credential`](../id-default-azure-credential/) (which credential signs in),
[`id-rbac`](../id-rbac/) (roles and scopes).
You need the Azure CLI and permission to create a resource group and to assign roles on it.

**Cost.** The resource and the Global Standard deployment have no fixed charge; you pay per token. The lab makes one or
two calls of a few hundred tokens, a fraction of a cent (about $0.75 per 1M input and $4.50 per 1M output tokens for
gpt-5.4-mini Global Standard, checked 2026-10-23; a real price depends on your country).

## Files

| File | What |
|---|---|
| `infra.bicep` | resource group scope: Foundry resource + project + `gpt-5.4-mini` (Global Standard), East US 2, no role assignment |
| `../../infra/modules/foundry.bicep` | the reusable module `infra.bicep` calls |
| `ask_the_shop.py` | the keyless call; asks "something gluten-free for breakfast under $5" |
| `.env.example` | `FOUNDRY_ENDPOINT`, `FOUNDRY_DEPLOYMENT` |

## Steps

```bash
cd lessons/ai-first-call-lab
pip install -r requirements.txt
```

1. **Deploy** (a Bicep deployment does not give anyone Foundry User, so the 403 is real). API keys are switched
   off in this lab (`disableLocalAuth`), so a role is the only way in.
   ```bash
   az group create -n rg-demo-cornercart-firstcall -l eastus2
   az deployment group create -g rg-demo-cornercart-firstcall -f infra.bicep
   ```
   Note the outputs `endpoint`, `deploymentName` and `accountId`:
   ```bash
   az deployment group show -g rg-demo-cornercart-firstcall -n infra --query properties.outputs
   ```
2. **Configure** the script, and sign in as the lab service principal (the variables from lesson 11):
   ```bash
   cp .env.example .env        # fill in endpoint and deployment from the outputs
   set -a; source .env; set +a
   export AZURE_TENANT_ID=<tenant id> AZURE_CLIENT_ID=<app id> AZURE_CLIENT_SECRET=<secret>
   ```
3. **Run it: 403.**
   ```bash
   python ask_the_shop.py
   ```
   ```
   403 Forbidden: authenticated, but this identity has no role on the Foundry resource.
   Assign Foundry User (53ca6127-db72-4b80-b1b0-d745d6d5456d) on the resource, wait a few minutes, run again.
   ```
   Even a Contributor, even an Owner, gets this: those roles manage the resource but have no data actions.
4. **Assign the role.** Portal: the Foundry resource, Access control (IAM), Add role assignment, **Foundry User**,
   Members: User, group, or service principal, pick the principal, Review + assign.
   The same from the CLI (the GUID works even in places that still show the old name, Azure AI User):
   ```bash
   az role assignment create --role 53ca6127-db72-4b80-b1b0-d745d6d5456d \
       --assignee <appId> --scope <accountId output>
   ```
5. **Wait, then run again: 200.** Role assignments can take up to 5 minutes to take effect.
   ```bash
   python ask_the_shop.py
   ```
   One sentence about three products from `data/products.json`.

If you created the resource in the portal yourself, you were given Foundry User automatically and will never see the
403. That is why the lab uses a service principal.

## How the call works

```python
token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
client = OpenAI(base_url=f"{endpoint}/openai/v1/", api_key=token_provider)
client.responses.create(model=deployment, input=...)
```

Pass the provider, not a token: the library fetches and refreshes tokens itself. `model` is the **deployment name**.
Chat Completions works the same way. Older Microsoft pages name other roles (Cognitive Services User, Cognitive
Services OpenAI User); they grant the same data actions, and this course uses Foundry User, the Foundry-specific one.
The real "Ask the shop" (search by meaning, then the model) comes in module 2.

## Clean-up

Delete the resource group; it takes the resource, project and deployment with it.
```bash
az group delete -n rg-demo-cornercart-firstcall --yes --no-wait
```
Foundry resource names are held for 48 hours after deletion (until purged), so the template adds a suffix from the
resource group id; do not reuse the same name right away.

## Tests

```bash
pytest tests/test_lesson_ask_the_shop.py
```
Offline, with a mocked client.
