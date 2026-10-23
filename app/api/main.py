"""CornerCart api: catalogue, search, ask, orders. Port 8000.

    uvicorn app.api.main:app --port 8000

/health says the process is alive; /ready says the data is loaded (the same two probes every
platform lab uses). The web app mounts this same router under /api.
"""

from __future__ import annotations

from fastapi import APIRouter, FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.shared.store import get_services

router = APIRouter()  # the data routes
probes = APIRouter()  # /health and /ready


class AskBody(BaseModel):
    q: str = Field(min_length=1, max_length=300, description="The question, in plain words")


class OrderLine(BaseModel):
    product_id: str
    qty: int = Field(ge=1, le=99)


class OrderBody(BaseModel):
    customer_id: str = "guest"
    lines: list[OrderLine] = Field(min_length=1, max_length=100)


def _with_rating(p: dict) -> dict:
    avg, count = get_services().catalog.rating(p["id"])
    return {**p, "rating_avg": avg, "rating_count": count}


@probes.get("/health")
def health() -> dict:
    return {"status": "ok"}


@probes.get("/ready")
def ready() -> dict:
    catalog = get_services().catalog
    if not catalog.ready():
        raise HTTPException(503, "data not loaded: run `python data/generate.py`")
    return {"status": "ready", "products": len(catalog.products()), "mode": "local"}


@router.get("/products")
def list_products(
    category: str | None = None,
    diet: list[str] | None = Query(None, description="gluten-free, vegan, sugar-free, nut-free"),
    max_price: float | None = Query(None, ge=0, description="US dollars"),
    q: str | None = None,
    limit: int = Query(24, ge=1, le=200),
    offset: int = Query(0, ge=0),
) -> dict:
    found = get_services().catalog.products(category, diet, max_price, q)
    return {
        "total": len(found),
        "limit": limit,
        "offset": offset,
        "items": [_with_rating(p) for p in found[offset : offset + limit]],
    }


@router.get("/products/{product_id}")
def get_product(product_id: str) -> dict:
    catalog = get_services().catalog
    p = catalog.product(product_id)
    if p is None:
        raise HTTPException(404, "no such product")
    return {**_with_rating(p), "reviews": catalog.reviews(product_id)[:10]}


@router.get("/products/{product_id}/reviews")
def product_reviews(product_id: str) -> list[dict]:
    catalog = get_services().catalog
    if catalog.product(product_id) is None:
        raise HTTPException(404, "no such product")
    return catalog.reviews(product_id)


@router.get("/search")
def search(q: str = Query(min_length=1), limit: int = Query(10, ge=1, le=50)) -> dict:
    found = get_services().catalog.products(q=q)
    return {"q": q, "mode": "keyword", "total": len(found), "items": [_with_rating(p) for p in found[:limit]]}


@router.post("/ask")
def ask(body: AskBody) -> dict:
    return get_services().asker.ask(body.q)


@router.get("/orders")
def list_orders(customer_id: str | None = None, limit: int = Query(50, ge=1, le=500)) -> list[dict]:
    return get_services().orders.list(customer_id)[:limit]


@router.get("/orders/{order_id}")
def get_order(order_id: str) -> dict:
    order = get_services().orders.get(order_id)
    if order is None:
        raise HTTPException(404, "no such order")
    return order


@router.post("/orders", status_code=201)
def create_order(body: OrderBody) -> dict:
    try:
        return get_services().orders.create(body.customer_id, [line.model_dump() for line in body.lines])
    except KeyError as e:
        raise HTTPException(422, f"unknown product {e.args[0]}") from e


app = FastAPI(title="CornerCart api", description="Demo data. Local mode.", version="0.1.0")
app.include_router(probes)
app.include_router(router)
