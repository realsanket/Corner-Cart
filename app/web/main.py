"""CornerCart web: the storefront. Plain HTML, a little CSS, no JavaScript. Port 8000.

    uvicorn app.web.main:app --port 8000

Serves the pages and also mounts the api under /api, so one command runs the whole local shop.
"""

from __future__ import annotations

import math
import uuid
from pathlib import Path
from urllib.parse import quote

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.main import probes
from app.api.main import router as api_router
from app.shared.basket import Basket, money
from app.shared.store import get_services

HERE = Path(__file__).resolve().parent
PAGE_SIZE = 24
COOKIE = "cc_basket"
DIETS = ["gluten-free", "vegan", "sugar-free", "nut-free"]
EXAMPLE_QUESTION = "something gluten-free for breakfast under $5"

templates = Jinja2Templates(directory=str(HERE / "templates"))
_SKIP = ("Gluten-Free ", "Frozen ", "Canned ", "Dried ", "Ground ", "Mild ", "Smoked ", "Mature ",
         "Zero Sugar ", "Whole ", "Plain ", "Salted ")  # fmt: skip


def initial(p: dict) -> str:
    """Tile letter: the first letter of the product's family name as a shopper reads it (Peanut Butter: P)."""
    name = p["family"]
    for skip in _SKIP:
        if name.startswith(skip) and len(name) > len(skip):
            name = name[len(skip) :]
    return name[0].upper()


templates.env.filters["initial"] = initial
templates.env.filters["usd"] = lambda v: f"${v:,.2f}"
templates.env.filters["when"] = lambda iso: iso.replace("T", " ").replace("Z", " UTC")

app = FastAPI(title="CornerCart web", description="Demo data. Local mode.", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(HERE / "static")), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(probes)  # /health and /ready at the root, for platform probes

_baskets: dict[str, Basket] = {}  # in memory, one per browser cookie (fine for a local demo)


def _basket(request: Request) -> tuple[str, Basket]:
    sid = request.cookies.get(COOKIE)
    if not sid or sid not in _baskets:
        sid = uuid.uuid4().hex
        _baskets[sid] = Basket()
    return sid, _baskets[sid]


def render(request: Request, name: str, status_code: int = 200, **ctx) -> HTMLResponse:
    sid, basket = _basket(request)
    catalog = get_services().catalog
    ctx.update(
        basket_count=basket.count(),
        categories=catalog.categories(),
        example_question=EXAMPLE_QUESTION,
        stars=lambda avg: "★" * round(avg) + "☆" * (5 - round(avg)),
    )
    response = templates.TemplateResponse(request, name, ctx, status_code=status_code)
    response.set_cookie(COOKIE, sid, httponly=True, samesite="lax")
    return response


def _card(p: dict) -> dict:
    avg, count = get_services().catalog.rating(p["id"])
    return {**p, "rating_avg": avg, "rating_count": count}


@app.get("/", response_class=HTMLResponse)
def storefront(request: Request, category: str | None = None, diet: str | None = None, page: int = 1):
    catalog = get_services().catalog
    diets = [diet] if diet in DIETS else []
    found = catalog.products(category=category, diet=diets)
    pages = max(1, math.ceil(len(found) / PAGE_SIZE))
    page = min(max(1, page), pages)
    items = [_card(p) for p in found[(page - 1) * PAGE_SIZE : page * PAGE_SIZE]]
    return render(request, "storefront.html", products=items, category=category, diet=diet, diets=DIETS,
                  page=page, pages=pages, total=len(found))  # fmt: skip


@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_page(request: Request, product_id: str):
    catalog = get_services().catalog
    p = catalog.product(product_id)
    if p is None:
        raise HTTPException(404, "no such product")
    return render(request, "product.html", p=_card(p), reviews=catalog.reviews(product_id)[:12])


@app.get("/ask", response_class=HTMLResponse)
def ask_page(request: Request, q: str = ""):
    result = get_services().asker.ask(q) if q.strip() else None
    if result:
        result["products"] = [_card(p) for p in result["products"]]
    return render(request, "ask.html", q=q, result=result)


@app.get("/basket", response_class=HTMLResponse)
def basket_page(request: Request):
    _, basket = _basket(request)
    by_id = get_services().catalog.by_id()
    return render(request, "basket.html", lines=basket.lines(by_id), total=basket.total(by_id))


@app.post("/basket/add")
def basket_add(request: Request, product_id: str = Form(), qty: int = Form(1)):
    if get_services().catalog.product(product_id) is None:
        raise HTTPException(404, "no such product")
    sid, basket = _basket(request)
    basket.add(product_id, qty)
    response = RedirectResponse("/basket", status_code=303)
    response.set_cookie(COOKIE, sid, httponly=True, samesite="lax")
    return response


@app.post("/basket/remove")
def basket_remove(request: Request, product_id: str = Form()):
    sid, basket = _basket(request)
    basket.remove(product_id)
    response = RedirectResponse("/basket", status_code=303)
    response.set_cookie(COOKIE, sid, httponly=True, samesite="lax")
    return response


@app.post("/checkout")
def checkout(request: Request):
    sid, basket = _basket(request)
    if not basket.items:
        return RedirectResponse("/basket", status_code=303)
    lines = [{"product_id": pid, "qty": qty} for pid, qty in basket.items.items()]
    order = get_services().orders.create("guest", lines)
    basket.clear()
    response = RedirectResponse(f"/orders/{quote(order['id'])}", status_code=303)
    response.set_cookie(COOKIE, sid, httponly=True, samesite="lax")
    return response


@app.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    return render(request, "orders.html", orders=get_services().orders.list()[:30])


@app.get("/orders/{order_id}", response_class=HTMLResponse)
def order_page(request: Request, order_id: str):
    order = get_services().orders.get(order_id)
    if order is None:
        raise HTTPException(404, "no such order")
    by_id = get_services().catalog.by_id()
    lines = [
        {**line, "name": by_id[line["product_id"]]["name"], "pack": by_id[line["product_id"]]["pack"],
         "line": money(round(line["unit_price_usd"] * 100) * line["qty"])}
        for line in order["lines"] if line["product_id"] in by_id
    ]  # fmt: skip
    steps = ["placed", "packed", "invoiced"]
    return render(request, "order.html", order=order, lines=lines, steps=steps,
                  reached=steps.index(order["status"]))  # fmt: skip
