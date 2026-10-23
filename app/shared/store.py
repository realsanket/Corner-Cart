"""The data seam. The apps talk to these small interfaces, never to files or Azure SDKs directly.

Today only local mode exists: it reads data/*.json into memory. When a lab switches a service on
(app/shared/config.py), the factory below returns that service's implementation instead; the apps
and their tests do not change.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path
from typing import Protocol

from app.shared import ask as ask_logic
from app.shared.basket import cents
from app.shared.config import Settings


class Catalog(Protocol):
    def ready(self) -> bool: ...
    def categories(self) -> list[str]: ...
    def products(self, category: str | None = None, diet: list[str] | None = None,
                 max_price: float | None = None, q: str | None = None) -> list[dict]: ...  # fmt: skip
    def product(self, product_id: str) -> dict | None: ...
    def by_id(self) -> dict[str, dict]: ...
    def reviews(self, product_id: str) -> list[dict]: ...
    def rating(self, product_id: str) -> tuple[float, int]: ...
    def ratings(self) -> dict[str, float]: ...


class Orders(Protocol):
    def list(self, customer_id: str | None = None) -> list[dict]: ...
    def get(self, order_id: str) -> dict | None: ...
    def create(self, customer_id: str, lines: list[dict]) -> dict: ...


class Asker(Protocol):
    def ask(self, question: str) -> dict: ...


def _load(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


class LocalCatalog:
    """Products and reviews from data/*.json, held in memory."""

    def __init__(self, data_dir: Path):
        self._products: list[dict] = []
        self._by_id: dict[str, dict] = {}
        self._reviews: dict[str, list[dict]] = {}
        self._ratings: dict[str, tuple[float, int]] = {}
        self._customers: dict[str, dict] = {}
        self._loaded = False
        try:
            self._products = _load(data_dir / "products.json")
            reviews = _load(data_dir / "reviews.json")
            self._customers = {c["id"]: c for c in _load(data_dir / "customers.json")}
        except (OSError, ValueError):
            return
        self._by_id = {p["id"]: p for p in self._products}
        for r in reviews:
            self._reviews.setdefault(r["product_id"], []).append(r)
        for pid, rs in self._reviews.items():
            self._ratings[pid] = (round(sum(r["rating"] for r in rs) / len(rs), 1), len(rs))
        self._loaded = bool(self._products)

    def ready(self) -> bool:
        return self._loaded

    def categories(self) -> list[str]:
        seen: list[str] = []
        for p in self._products:
            if p["category"] not in seen:
                seen.append(p["category"])
        return seen

    def products(self, category=None, diet=None, max_price=None, q=None) -> list[dict]:
        out = self._products
        if category:
            out = [p for p in out if p["category"].lower() == category.lower()]
        if diet:
            out = [p for p in out if all(d in p["diet"] for d in diet)]
        if max_price is not None:
            out = [p for p in out if p["price_usd"] <= max_price]
        if q:
            parsed = ask_logic.parse_query(q)
            hits = ask_logic.search(out, parsed, {k: v[0] for k, v in self._ratings.items()}, limit=len(out))
            out = hits
        return out

    def product(self, product_id: str) -> dict | None:
        return self._by_id.get(product_id)

    def by_id(self) -> dict[str, dict]:
        return self._by_id

    def reviews(self, product_id: str) -> list[dict]:
        rs = sorted(self._reviews.get(product_id, []), key=lambda r: r["created_at"], reverse=True)
        return [{**r, "customer": self._customers.get(r["customer_id"], {}).get("name", "A customer")} for r in rs]

    def rating(self, product_id: str) -> tuple[float, int]:
        return self._ratings.get(product_id, (0.0, 0))

    def ratings(self) -> dict[str, float]:
        return {k: v[0] for k, v in self._ratings.items()}


class LocalOrders:
    """The sample orders from data/orders.json, plus orders placed while the server runs (in memory)."""

    def __init__(self, data_dir: Path, catalog: LocalCatalog):
        try:
            self._orders = _load(data_dir / "orders.json")
        except (OSError, ValueError):
            self._orders = []
        self._catalog = catalog
        self._next = len(self._orders) + 1

    def list(self, customer_id=None) -> list[dict]:
        orders = [o for o in self._orders if customer_id in (None, o["customer_id"])]
        return sorted(orders, key=lambda o: o["created_at"], reverse=True)

    def get(self, order_id: str) -> dict | None:
        return next((o for o in self._orders if o["id"] == order_id), None)

    def create(self, customer_id: str, lines: list[dict]) -> dict:
        built, total = [], 0
        for line in lines:
            p = self._catalog.product(line["product_id"])
            if p is None:
                raise KeyError(line["product_id"])
            qty = int(line["qty"])
            built.append({"product_id": p["id"], "qty": qty, "unit_price_usd": p["price_usd"]})
            total += cents(p["price_usd"]) * qty
        order = {
            "id": f"o{self._next:05d}",
            "customer_id": customer_id,
            "status": "placed",
            "created_at": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lines": built,
            "total_usd": round(total / 100, 2),
        }
        self._next += 1
        self._orders.append(order)
        return order


class LocalAsker:
    """Keyword mode: filters read from the text, top 3, one templated sentence."""

    def __init__(self, catalog: LocalCatalog):
        self._catalog = catalog

    def ask(self, question: str) -> dict:
        return ask_logic.ask(self._catalog.products(), question, self._catalog.ratings())


class Services:
    def __init__(self, settings: Settings):
        self.settings = settings
        for name, value in (("catalog", settings.catalog), ("orders", settings.orders),
                            ("ask", settings.ask), ("cache", settings.cache)):  # fmt: skip
            if value != "local":
                raise NotImplementedError(
                    f"CORNERCART_{name.upper()}={value}: only local mode exists so far. "
                    "The Azure version arrives in the lab that teaches it."
                )
        self.catalog = LocalCatalog(settings.data_dir)
        self.orders = LocalOrders(settings.data_dir, self.catalog)
        self.asker = LocalAsker(self.catalog)


@lru_cache(maxsize=1)
def get_services() -> Services:
    return Services(Settings.from_env())
