# Lesson 11: DefaultAzureCredential, the order it tries

**Goal.** See that the same code signs in on your laptop and in Azure. `DefaultAzureCredential` tries each
credential in a fixed order and uses the first one that works. This lab shows which one won, and how to force the
result you want.

**Prerequisites.** [`id-managed-identity`](../id-managed-identity/) (the identity that wins inside Azure).
You need Python 3.12+ and the Azure CLI, signed in (`az login --use-device-code`) or a lab service principal.

**Cost.** $0. It asks for a token; no Azure resource is created, there is no resource group.

## The order (azure-identity 1.26.0)

1. Environment (a service principal from `AZURE_TENANT_ID`, `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`)
2. Workload Identity
3. Managed Identity
4. Shared Token Cache (Windows only)
5. Visual Studio Code (needs `azure-identity-broker`)
6. Azure CLI
7. Azure PowerShell
8. Azure Developer CLI
9. Interactive browser (off by default)
10. Broker (Windows / WSL, needs `azure-identity-broker`)

Some course material lists a shorter chain with azd before PowerShell. The SDK's own docs and source put
**PowerShell before azd**; `whoami.py` follows the SDK, and a test checks the list against the installed library.

## Steps

```bash
cd lessons/id-default-azure-credential
pip install -r requirements.txt
```

1. **Your own login wins.** No `AZURE_*` variables set:
   ```bash
   az login --use-device-code
   python whoami.py
   ```
   Output ends with `Winner: AzureCliCredential`.
2. **An environment variable outranks your login.** Export the lab service principal's three variables:
   ```bash
   export AZURE_TENANT_ID=<tenant id>
   export AZURE_CLIENT_ID=<app id>
   export AZURE_CLIENT_SECRET=<secret>
   python whoami.py
   ```
   Now `Winner: EnvironmentCredential`, because it comes first, even though you are still logged in with `az login`.
3. **Production code never falls back to your login.**
   ```bash
   AZURE_TOKEN_CREDENTIALS=prod python whoami.py
   ```
   On a laptop with no variables and no managed identity this fails and says what each credential answered
   (`no response from the IMDS endpoint`). `prod` keeps only Environment, Workload Identity and Managed Identity.
4. **Unset the variables.**
   ```bash
   unset AZURE_TENANT_ID AZURE_CLIENT_ID AZURE_CLIENT_SECRET
   ```

Inside Azure (an App Service, a Container App) the same unchanged script prints `ManagedIdentityCredential`.

## Take control

- `AZURE_TOKEN_CREDENTIALS=prod` or `dev` (azure-identity 1.23.0 and later), or one credential's name (1.24.0 and later).
- `DefaultAzureCredential(exclude_cli_credential=True)` and the other `exclude_*` flags.
- `ChainedTokenCredential(...)` for a chain of your own.

Why bother in production: speed (the chain tries credentials that cannot work) and surprises, such as environment
variables set on the host that silently change who you are.

## What the script does

`whoami.py` turns on the `azure.identity` logger at INFO. The library logs
`DefaultAzureCredential acquired a token from AzureCliCredential`; the script catches that line and prints it in
plain words with the chain, the tenant and the app id (masked: `72f9...db47`). The token is never printed.

## Clean-up

Nothing was created in Azure. Unset the `AZURE_*` variables (step 4) and, if you want, `az logout`.

## Tests

```bash
pytest tests/test_lesson_whoami.py
```
Offline, with a fake credential.
