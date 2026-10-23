# CornerCart

**Your corner shop, online.** About 1,000 everyday groceries and household basics, a basket, orders, reviews and an
**"Ask the shop"** box: type *"something gluten-free for breakfast under $5"* and get three products and one sentence.

CornerCart is the one example app for Sanket's YouTube series on Azure (AI-200 first). Every lesson builds one piece of
it. This repo runs **locally with no Azure at all**; each Azure service switches on in the lesson that teaches it.

## Run it locally (3 commands)

Needs Python 3.12 or newer. No keys, no cloud account.

```bash
pip install -r requirements.txt
python data/generate.py
uvicorn app.web.main:app --port 8000
```

Open <http://localhost:8000>. Try the Ask box with
[something gluten-free for breakfast under $5](http://localhost:8000/ask?q=something+gluten-free+for+breakfast+under+%245).
Local mode answers in **keyword mode** (words plus filters such as "under $5", "vegan", "gluten-free"); search by meaning
arrives in the data lessons.

The api alone: `uvicorn app.api.main:app --port 8000` (docs at `/docs`). The web app also serves it under `/api`.
Probes for every platform: `/health` (alive) and `/ready` (data loaded).

```bash
curl -s localhost:8000/ready
curl -s -X POST localhost:8000/api/ask -H 'content-type: application/json' \
     -d '{"q": "something gluten-free for breakfast under $5"}'
```

Check your tools (Azure CLI, Bicep, Docker, Functions Core Tools, Azurite, kubectl, psql...): `python scripts/check_tools.py`.
In GitHub Codespaces (Code, then Codespaces) the dev container installs all of them.

Tests and lint: `pytest` and `ruff check .`

## Demo data

Everything in `data/` is **invented demo data**, made by `data/generate.py` with one fixed seed: the same seed always gives
the same files. No real brands. Prices are in US dollars (a real price depends on your country), packs are metric
("1 L", "500 g"), times are UTC.

| File | What | Size |
|---|---|---|
| `products.json` | 1,000 products: price, pack, stock, diet tags, a short note | ~310 KB |
| `customers.json` | 200 customers, names from many cultures, a city and country each | ~20 KB |
| `reviews.json` | 3,000 reviews linked to products and customers | ~550 KB |
| `orders.json` | 300 sample orders | ~100 KB |
| `shop-guide/*.md` | a short shop guide (storage, delivery, returns, labels) | ~7 KB |
| `price_history.csv` | ~365,000 rows, **not committed**: `python data/generate.py --price-history` | ~8 MB |

## Layout

```
app/
  web/            storefront: plain HTML + a little CSS, no JavaScript framework (port 8000)
  api/            catalogue, search, ask, orders; /health and /ready (port 8000)
  shared/         config.py (one switch per Azure service), store.py (the data seam), ask.py, basket.py
data/             generate.py (fixed seed), the generated JSON, shop-guide/
scripts/          check_tools.py (the bench check)
tests/            pytest: generator, ask, api, web, bench check
.devcontainer/    Python 3.12, Azure CLI + Bicep + extensions, Docker, Functions Core Tools, Azurite, kubectl, psql
.github/workflows ci.yml: ruff + pytest on every push (no Azure, no secrets)
```

Lab folders so far: `lessons/id-default-azure-credential/`, `lessons/ai-first-call-lab/`; Bicep modules in `infra/modules/`. Coming: `worker/`, `functions/`, more `lessons/<lesson-id>/`.

## Lessons

The lesson index is generated later.
