import json
from itertools import islice

import generate


def test_same_seed_same_data():
    assert generate.build_all() == generate.build_all()
    assert generate.dumps_records(generate.build_all()["products"]) == generate.dumps_records(
        generate.build_all()["products"]
    )


def test_sizes_and_links():
    data = generate.build_all()
    assert len(data["products"]) == 1000
    assert len(data["customers"]) == 200
    assert len(data["reviews"]) == 3000
    assert 200 <= len(data["orders"]) <= 500
    product_ids = {p["id"] for p in data["products"]}
    customer_ids = {c["id"] for c in data["customers"]}
    assert all(r["product_id"] in product_ids and r["customer_id"] in customer_ids for r in data["reviews"])
    assert all(1 <= r["rating"] <= 5 for r in data["reviews"])
    assert len({p["name"] for p in data["products"]}) == 1000


def test_product_fields():
    for p in generate.build_all()["products"]:
        assert set(p) >= {"id", "name", "category", "price_usd", "pack", "stock", "diet", "note"}
        assert p["price_usd"] > 0 and p["stock"] >= 0
        assert set(p["diet"]) <= {"gluten-free", "vegan", "sugar-free", "nut-free"}


def test_committed_files_match_generator():
    for name, records in generate.build_all().items():
        committed = (generate.DATA_DIR / f"{name}.json").read_text(encoding="utf-8")
        assert committed == generate.dumps_records(records), f"{name}.json is stale: run python data/generate.py"
        assert json.loads(committed) == records


def test_shop_guide_pages():
    pages = list((generate.DATA_DIR / "shop-guide").glob("*.md"))
    assert 3 <= len(pages) <= 5


def test_price_history_is_deterministic_and_the_right_size():
    products = generate.build_all()["products"]
    first = list(islice(generate.iter_price_history(products), 400))
    assert first == list(islice(generate.iter_price_history(products), 400))
    assert len(products) * generate.PRICE_DAYS == 365_000
    assert sum(1 for r in first if r[0] == products[0]["id"]) == generate.PRICE_DAYS
