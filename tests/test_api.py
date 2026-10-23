def test_health(api):
    assert api.get("/health").json() == {"status": "ok"}


def test_ready_when_data_is_loaded(api):
    r = api.get("/ready")
    assert r.status_code == 200
    assert r.json()["products"] == 1000


def test_ready_is_503_without_data(monkeypatch, tmp_path):
    from fastapi.testclient import TestClient

    from app.api.main import app
    from app.shared.store import get_services

    monkeypatch.setenv("CORNERCART_DATA_DIR", str(tmp_path))
    get_services.cache_clear()
    try:
        assert TestClient(app).get("/ready").status_code == 503
    finally:
        get_services.cache_clear()


def test_products_and_detail(api):
    page = api.get("/products", params={"category": "Breakfast", "limit": 5}).json()
    assert page["total"] > 50 and len(page["items"]) == 5
    pid = page["items"][0]["id"]
    detail = api.get(f"/products/{pid}").json()
    assert detail["id"] == pid and "reviews" in detail
    assert api.get("/products/nope").status_code == 404


def test_products_filters(api):
    params = {"diet": ["vegan", "gluten-free"], "max_price": 2, "limit": 200}
    items = api.get("/products", params=params).json()["items"]
    assert items and all(p["price_usd"] <= 2 and "vegan" in p["diet"] for p in items)


def test_search(api):
    body = api.get("/search", params={"q": "basmati rice"}).json()
    assert body["items"] and all("Rice" in p["name"] for p in body["items"][:3])


def test_ask_endpoint(api):
    r = api.post("/ask", json={"q": "something gluten-free for breakfast under $5"})
    assert r.status_code == 200
    assert len(r.json()["products"]) == 3
    assert api.post("/ask", json={"q": ""}).status_code == 422


def test_orders(api):
    assert api.get("/orders", params={"limit": 3}).json()
    pid = api.get("/products").json()["items"][0]
    price = pid["price_usd"]
    r = api.post("/orders", json={"lines": [{"product_id": pid["id"], "qty": 3}]})
    assert r.status_code == 201
    order = r.json()
    assert order["status"] == "placed" and order["total_usd"] == round(price * 3, 2)
    assert api.get(f"/orders/{order['id']}").json()["id"] == order["id"]
    assert api.post("/orders", json={"lines": [{"product_id": "nope", "qty": 1}]}).status_code == 422
