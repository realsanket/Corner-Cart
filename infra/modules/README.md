# infra/modules

Reusable Bicep modules, one per Azure service, used by the lab folders.

| Module | What | Used by |
|---|---|---|
| `foundry.bicep` | Foundry resource (AIServices) + project + one model deployment, no role assignment | `lessons/ai-first-call-lab/infra.bicep` |

Check a module: `az bicep build --file infra/modules/foundry.bicep --stdout > /dev/null`
