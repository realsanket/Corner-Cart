"""Ask the shop, with a model: the first keyless call to a Foundry deployment.

    FOUNDRY_ENDPOINT    https://<resource>.openai.azure.com   (the `endpoint` output of infra.bicep)
    FOUNDRY_DEPLOYMENT  the deployment name your code asks for (default: gpt-5.4-mini)

The shop's real "Ask" (search by meaning, then the model) comes in module 2. Here the prompt holds
three demo products picked by a plain filter, so the model has something true to talk about.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import openai
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

QUESTION = "something gluten-free for breakfast under $5"
PRODUCTS = Path(__file__).resolve().parents[2] / "data" / "products.json"
FOUNDRY_USER_ROLE_ID = "53ca6127-db72-4b80-b1b0-d745d6d5456d"
INSTRUCTIONS = (
    "You are the assistant of CornerCart, a small online grocery shop. "
    "Answer in ONE sentence, recommending only products from the list, with their price in US dollars."
)


def demo_products(path: Path = PRODUCTS, count: int = 3) -> list[dict]:
    """Three in-stock products that fit the question, each from a different category."""
    products = json.loads(path.read_text(encoding="utf-8"))
    fits = [
        p for p in products
        if "gluten-free" in p["diet"] and "breakfast" in p["meals"] and p["price_usd"] < 5 and p["stock"] > 0
    ]  # fmt: skip
    picked: dict[str, dict] = {}
    for product in fits:
        picked.setdefault(product["category"], product)
    return list(picked.values())[:count]


def build_prompt(question: str, products: list[dict]) -> str:
    lines = [f"- {p['name']} ({p['pack']}), ${p['price_usd']:.2f}: {p['note']}" for p in products]
    return f"Customer asks: {question}\n\nProducts in stock:\n" + "\n".join(lines)


def make_client(endpoint: str) -> OpenAI:
    # The provider, not a token: the library asks for a fresh token whenever the old one is near its end.
    token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")
    return OpenAI(base_url=f"{endpoint.rstrip('/')}/openai/v1/", api_key=token_provider)


def ask(client: OpenAI, deployment: str, question: str = QUESTION) -> str:
    response = client.responses.create(
        model=deployment,  # the deployment name, not the model name
        instructions=INSTRUCTIONS,
        input=build_prompt(question, demo_products()),
    )
    return response.output_text.strip()


def main(client: OpenAI | None = None) -> int:
    endpoint = os.environ.get("FOUNDRY_ENDPOINT", "")
    deployment = os.environ.get("FOUNDRY_DEPLOYMENT", "gpt-5.4-mini")
    if client is None and not endpoint:
        print("FOUNDRY_ENDPOINT is not set. Copy .env.example to .env, fill it in, and load it.")
        return 2
    print(f'Asking the shop: "{QUESTION}"\n')
    try:
        print(ask(client or make_client(endpoint), deployment))
    except openai.PermissionDeniedError:
        print("403 Forbidden: authenticated, but this identity has no role on the Foundry resource.")
        print(f"Assign Foundry User ({FOUNDRY_USER_ROLE_ID}) on the resource, wait a few minutes, run again.")
        return 1
    except openai.NotFoundError:
        print(f'404 Not Found: no deployment called "{deployment}" at this endpoint. Check FOUNDRY_DEPLOYMENT.')
        return 1
    except (openai.AuthenticationError, ClientAuthenticationError) as error:
        print(f"401 Unauthorized: no valid sign-in ({type(error).__name__}).")
        print("Check which credential is used: python ../id-default-azure-credential/whoami.py")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
