import base64
import json
import logging
from types import SimpleNamespace

from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential

from tests.lab_loader import load

whoami = load("id-default-azure-credential", "whoami")
TENANT = "72f988bf-86f1-41af-91ab-2d7cd011db47"
APP = "04b07795-8ddb-461a-bbee-02f9e1bf7b46"


def fake_jwt(**claims) -> str:
    body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    return f"header.{body}.signature"


class FakeCredential:
    """Behaves like DefaultAzureCredential: logs which badge worked, returns a token."""

    def __init__(self, winner: str, **claims):
        self.winner, self.claims = winner, claims

    def get_token(self, *scopes):
        assert scopes == ("https://management.azure.com/.default",)
        logging.getLogger("azure.identity._credentials.default").info(
            "%s acquired a token from %s", "DefaultAzureCredential", self.winner
        )
        return SimpleNamespace(token=fake_jwt(**self.claims), expires_on=0)


def test_names_the_winner_and_masks_ids(capsys):
    cred = FakeCredential("AzureCliCredential", tid=TENANT, appid=APP, idtyp="user")
    assert whoami.main(cred) == 0
    out = capsys.readouterr().out
    assert "Winner: AzureCliCredential" in out
    assert "az login" in out
    assert "a person" in out
    assert "72f9...db47" in out and "04b0...7b46" in out
    assert TENANT not in out and APP not in out
    assert "signature" not in out  # the token is never printed


def test_service_principal_reads_as_environment_credential(capsys):
    cred = FakeCredential("EnvironmentCredential", tid=TENANT, azp=APP, idtyp="app")
    whoami.main(cred)
    out = capsys.readouterr().out
    assert "Winner: EnvironmentCredential" in out
    assert "AZURE_CLIENT_SECRET" in out
    assert "an app (service principal or managed identity)" in out
    assert "<-- this one worked" in out.split("EnvironmentCredential")[1].splitlines()[0]


def test_failure_is_explained_not_a_stack_trace(capsys):
    class Broken:
        def get_token(self, *scopes):
            raise ClientAuthenticationError(
                "DefaultAzureCredential failed to retrieve a token.\n"
                "ManagedIdentityCredential: no response from the IMDS endpoint."
            )

    assert whoami.main(Broken()) == 1
    out = capsys.readouterr().out
    assert "No credential in the chain could get a token" in out
    assert "no response from the IMDS endpoint" in out
    assert "az login --use-device-code" in out


def test_mask():
    assert whoami.mask(None) == "(none)"
    assert whoami.mask("abc") == "****"
    assert whoami.mask(TENANT) == "72f9...db47"


def test_chain_order_matches_the_installed_library():
    """The order on screen must be the library's real order (azure-identity pinned in requirements.txt)."""
    # Without its env vars, WorkloadIdentityCredential is replaced by a placeholder (FailedDACCredential).
    real = [
        type(c).__name__.replace("FailedDACCredential", "WorkloadIdentityCredential")
        for c in DefaultAzureCredential().credentials
    ]
    shown = [name for name, _ in whoami.CHAIN]
    assert real, "the chain is empty"
    positions = [shown.index(name) for name in real]  # every real credential is in our list ...
    assert positions == sorted(positions)  # ... in the same order
    assert shown[:3] == ["EnvironmentCredential", "WorkloadIdentityCredential", "ManagedIdentityCredential"]
    assert shown.index("AzurePowerShellCredential") < shown.index("AzureDeveloperCliCredential")
