"""The basket: product ids and quantities, money in whole cents so totals are exact."""

from __future__ import annotations

from dataclasses import dataclass, field

MAX_QTY = 99


def cents(price_usd: float) -> int:
    return round(price_usd * 100)


def money(total_cents: int) -> str:
    return f"${total_cents / 100:,.2f}"


@dataclass
class Basket:
    items: dict[str, int] = field(default_factory=dict)

    def add(self, product_id: str, qty: int = 1) -> None:
        self.items[product_id] = min(MAX_QTY, self.items.get(product_id, 0) + max(1, qty))

    def remove(self, product_id: str) -> None:
        self.items.pop(product_id, None)

    def lines(self, products_by_id: dict[str, dict]) -> list[dict]:
        out = []
        for pid, qty in self.items.items():
            p = products_by_id.get(pid)
            if p is None:
                continue
            line_cents = cents(p["price_usd"]) * qty
            out.append({"product": p, "qty": qty, "line_cents": line_cents, "line": money(line_cents)})
        return out

    def total_cents(self, products_by_id: dict[str, dict]) -> int:
        return sum(line["line_cents"] for line in self.lines(products_by_id))

    def total(self, products_by_id: dict[str, dict]) -> str:
        return money(self.total_cents(products_by_id))

    def count(self) -> int:
        return sum(self.items.values())

    def clear(self) -> None:
        self.items.clear()
