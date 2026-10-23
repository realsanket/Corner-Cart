"""Settings, read from environment variables.

Local mode needs none of them. Each Azure service gets its own switch; a lab turns one on by setting
its variable, and everything else keeps running locally:

    CORNERCART_CATALOG = local | postgres      products and reviews     (M2)
    CORNERCART_ORDERS  = local | cosmos        orders and baskets       (M2)
    CORNERCART_ASK     = local | foundry       "Ask the shop"           (M2)
    CORNERCART_CACHE   = local | redis         the hot catalogue page   (M2)
    CORNERCART_DATA_DIR                        where products.json etc. live (default: ./data)
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    catalog: str = "local"
    orders: str = "local"
    ask: str = "local"
    cache: str = "local"
    data_dir: Path = REPO_ROOT / "data"

    @classmethod
    def from_env(cls) -> Settings:
        env = os.environ.get
        return cls(
            catalog=env("CORNERCART_CATALOG", "local").lower(),
            orders=env("CORNERCART_ORDERS", "local").lower(),
            ask=env("CORNERCART_ASK", "local").lower(),
            cache=env("CORNERCART_CACHE", "local").lower(),
            data_dir=Path(env("CORNERCART_DATA_DIR", str(REPO_ROOT / "data"))),
        )
