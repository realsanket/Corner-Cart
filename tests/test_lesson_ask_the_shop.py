from types import SimpleNamespace

import httpx
import openai

from tests.lab_loader import load

shop = load("ai-first-call-lab", "ask_the_shop")


def api_error(cls, status):
    request = httpx.Request("POST", "https://example.openai.azure.com/openai/v1/responses")
    return cls("boom", response=httpx.Response(status, request=request), body=None)


class FakeClient:
    def __init__(self, result=None, error=None):
        self.calls = []
        self.responses = SimpleNamespace(create=self._create)
        self._result, self._error = result, error

    def _create(self, **kwargs):
        self.calls.append(kwargs)
        if self._error:
            raise self._error
        return SimpleNamespace(output_text=self._result)


def test_demo_products_fit_the_question():
    products = shop.demo_products()
    assert len(products) == 3
    assert len({p["category"] for p in products}) == 3
    for p in products:
        assert "gluten-free" in p["diet"] and "breakfast" in p["meals"] and p["price_usd"] < 5


def test_prompt_holds_the_question_and_the_three_products():
    products = shop.demo_products()
    prompt = shop.build_prompt(shop.QUESTION, products)
    assert "something gluten-free for breakfast under $5" in prompt
    for p in products:
        assert p["name"] in prompt and f"${p['price_usd']:.2f}" in prompt
    assert prompt.count("\n- ") == 3


def test_success_prints_the_one_sentence_and_uses_the_deployment_name(monkeypatch, capsys):
    monkeypatch.setenv("FOUNDRY_DEPLOYMENT", "my-deployment")
    client = FakeClient(result="  Try the gluten-free oats at $2.10.  ")
    assert shop.main(client) == 0
    assert "Try the gluten-free oats at $2.10." in capsys.readouterr().out
    call = client.calls[0]
    assert call["model"] == "my-deployment"
    assert "something gluten-free for breakfast under $5" in call["input"]


def test_403_is_a_short_message_not_a_stack_trace(capsys):
    client = FakeClient(error=api_error(openai.PermissionDeniedError, 403))
    assert shop.main(client) == 1
    out = capsys.readouterr().out
    assert out.startswith("Asking the shop")
    assert "403 Forbidden: authenticated, but this identity has no data role on the Foundry resource" in out
    assert "Foundry User" in out and "53ca6127-db72-4b80-b1b0-d745d6d5456d" in out
    assert "Traceback" not in out


def test_401_permission_denied_is_the_missing_data_role(capsys):
    """Seen live: the service answers 401 with code PermissionDenied when the sign-in works but the data role is missing."""
    request = httpx.Request("POST", "https://example.openai.azure.com/openai/v1/responses")
    body = {"code": "PermissionDenied", "message": "The principal lacks the required data action"}
    error = openai.AuthenticationError("boom", response=httpx.Response(401, request=request), body=body)
    assert shop.main(FakeClient(error=error)) == 1
    out = capsys.readouterr().out
    assert "401 PermissionDenied: authenticated, but this identity has no data role on the Foundry resource" in out
    assert "53ca6127-db72-4b80-b1b0-d745d6d5456d" in out


def test_404_names_the_deployment(monkeypatch, capsys):
    monkeypatch.setenv("FOUNDRY_DEPLOYMENT", "nope")
    assert shop.main(FakeClient(error=api_error(openai.NotFoundError, 404))) == 1
    assert '"nope"' in capsys.readouterr().out


def test_missing_endpoint_is_explained(monkeypatch, capsys):
    monkeypatch.delenv("FOUNDRY_ENDPOINT", raising=False)
    assert shop.main() == 2
    assert "FOUNDRY_ENDPOINT is not set" in capsys.readouterr().out


def test_client_is_keyless(monkeypatch):
    seen = {}
    monkeypatch.setattr(shop, "DefaultAzureCredential", lambda: "credential")
    monkeypatch.setattr(
        shop, "get_bearer_token_provider", lambda cred, scope: seen.update(cred=cred, scope=scope) or (lambda: "tok")
    )
    client = shop.make_client("https://ai-cornercart-abc12.openai.azure.com/")
    assert seen == {"cred": "credential", "scope": "https://ai.azure.com/.default"}
    assert str(client.base_url) == "https://ai-cornercart-abc12.openai.azure.com/openai/v1/"
