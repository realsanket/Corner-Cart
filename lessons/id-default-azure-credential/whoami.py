"""Which credential did DefaultAzureCredential use?

Asks Azure for a token (no Azure resource needed) and says, in plain words, which badge in the
chain worked and who you are signed in as. The token itself is never printed.

    python whoami.py                          # the whole chain, as a laptop would use it
    AZURE_TOKEN_CREDENTIALS=prod python whoami.py   # only the deployed-service credentials
"""

from __future__ import annotations

import base64
import json
import logging
import sys

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential

# The scope of the Azure management plane. Any valid scope would do; this one always exists.
SCOPE = "https://management.azure.com/.default"

# The order azure-identity 1.26.0 tries them (DefaultAzureCredential docstring, "Credential chains" page).
# A test checks this list against the library, so it cannot drift.
CHAIN = [
    ("EnvironmentCredential", "a service principal from AZURE_* variables"),
    ("WorkloadIdentityCredential", "a Kubernetes service account"),
    ("ManagedIdentityCredential", "the identity of an Azure resource"),
    ("SharedTokenCacheCredential", "a shared sign-in cache (works on Windows only)"),
    ("VisualStudioCodeCredential", "needs azure-identity-broker"),
    ("AzureCliCredential", "your own `az login`"),
    ("AzurePowerShellCredential", "your own Connect-AzAccount"),
    ("AzureDeveloperCliCredential", "your own `azd auth login`"),
    ("InteractiveBrowserCredential", "off by default"),
    ("BrokerCredential", "Windows / WSL, needs azure-identity-broker"),
]

MEANING = {
    "EnvironmentCredential": "A service principal: AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET are set.",
    "WorkloadIdentityCredential": "A Kubernetes pod using a federated service account.",
    "ManagedIdentityCredential": "The managed identity of the Azure resource this code runs on.",
    "AzureCliCredential": "You: the account you signed in with `az login`.",
    "AzurePowerShellCredential": "You: the account you signed in with Connect-AzAccount.",
    "AzureDeveloperCliCredential": "You: the account you signed in with `azd auth login`.",
}


def mask(value: str | None) -> str:
    """72f9...88ab: enough to recognise an id, not enough to share it."""
    if not value:
        return "(none)"
    return f"{value[:4]}...{value[-4:]}" if len(value) > 10 else "****"


def token_claims(token: str) -> dict:
    """Read the payload of a JWT. No signature check: we only want to show who it says it is."""
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload))
    except (IndexError, ValueError):
        return {}


class _Winner(logging.Handler):
    """Listens to the azure.identity logger for: 'DefaultAzureCredential acquired a token from X'."""

    def __init__(self) -> None:
        super().__init__(logging.INFO)
        self.name_of_winner: str | None = None

    def emit(self, record: logging.LogRecord) -> None:
        if "acquired a token from" in str(record.msg) and len(record.args or ()) == 2:
            self.name_of_winner = str(record.args[1])


def show_chain(winner: str | None) -> None:
    print("The chain, in the order it is tried:")
    for number, (name, hint) in enumerate(CHAIN, start=1):
        mark = "  <-- this one worked" if name == winner else ""
        print(f"  {number:>2}. {name:<30} {hint}{mark}")
    print()


def report(winner: str | None, claims: dict) -> None:
    show_chain(winner)
    print(f"Winner: {winner or 'unknown'}")
    print(f"  {MEANING.get(winner or '', '')}".rstrip())
    kind = "an app (service principal or managed identity)" if claims.get("idtyp") == "app" else "a person"
    print(f"Signed in as {kind}")
    print(f"  tenant : {mask(claims.get('tid'))}")
    print(f"  app id : {mask(claims.get('appid') or claims.get('azp'))}")


def main(credential: DefaultAzureCredential | None = None) -> int:
    logger = logging.getLogger("azure.identity")
    logger.setLevel(logging.INFO)
    winner = _Winner()
    logger.addHandler(winner)
    try:
        credential = credential or DefaultAzureCredential()
        print("Asking DefaultAzureCredential for a token...\n")
        token = credential.get_token(SCOPE)
    except ClientAuthenticationError as error:
        print("No credential in the chain could get a token.\n")
        show_chain(None)
        print("What each one said:")
        for line in str(error).splitlines()[1:]:
            if line.strip():
                print(f"  {line.strip()[:160]}")
        print("\nOn a laptop or codespace: az login --use-device-code")
        return 1
    finally:
        logger.removeHandler(winner)
    name = winner.name_of_winner or type(getattr(credential, "_successful_credential", None)).__name__
    report(name if name != "NoneType" else None, token_claims(token.token))
    return 0


if __name__ == "__main__":
    sys.exit(main())
