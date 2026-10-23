import re

from app.shared.basket import Basket


def test_basket_total_is_exact():
    by_id = {"a": {"price_usd": 0.1}, "b": {"price_usd": 1.99}}
    basket = Basket()
    basket.add("a", 3)
    basket.add("b")
    basket.add("b")
    assert basket.count() == 5
    assert basket.total(by_id) == "$4.28"
    basket.remove("a")
    assert basket.total(by_id) == "$3.98"


def test_pages_render(web):
    for url in ["/", "/?category=Breakfast&diet=vegan", "/product/p0001", "/basket", "/orders", "/orders/o00001"]:
        assert web.get(url).status_code == 200, url
    assert web.get("/product/zzz").status_code == 404
    assert "demo data" in web.get("/").text


def test_probes_at_the_root_and_api_under_api(web):
    assert web.get("/health").status_code == 200
    assert web.get("/ready").status_code == 200
    assert web.get("/api/products?limit=1").status_code == 200


def test_ask_page(web):
    page = web.get("/ask", params={"q": "something gluten-free for breakfast under $5"}).text
    assert "keyword mode" in page
    assert len(re.findall(r'class="card"', page)) == 3


def test_basket_flow_in_the_browser(web):
    web.post("/basket/add", data={"product_id": "p0001", "qty": 2}, follow_redirects=False)
    web.post("/basket/add", data={"product_id": "p0002", "qty": 1})
    page = web.get("/basket").text
    p1 = web.get("/api/products/p0001").json()["price_usd"]
    p2 = web.get("/api/products/p0002").json()["price_usd"]
    assert f"${p1 * 2 + p2:,.2f}" in page
    web.post("/basket/remove", data={"product_id": "p0001"})
    assert f"${p2:,.2f}" in web.get("/basket").text
    r = web.post("/checkout", follow_redirects=False)
    assert r.status_code == 303 and r.headers["location"].startswith("/orders/o")
    assert web.get(r.headers["location"]).status_code == 200
