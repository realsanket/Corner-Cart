from app.shared.ask import parse_query

QUESTION = "something gluten-free for breakfast under $5"


def test_parse_query_reads_the_filters():
    q = parse_query(QUESTION)
    assert q.diets == ["gluten-free"]
    assert q.meals == ["breakfast"]
    assert q.max_price == 5.0
    assert q.words == []


def test_parse_other_phrasings():
    q = parse_query("vegan pasta below 3 dollars or less, nut free")
    assert q.diets == ["vegan", "nut-free"]
    assert q.words == ["pasta"]


def test_ask_returns_three_gluten_free_breakfast_products_under_5(services):
    result = services.asker.ask(QUESTION)
    assert result["mode"] == "keyword"
    products = result["products"]
    assert len(products) == 3
    assert len({p["family"] for p in products}) == 3
    for p in products:
        assert "gluten-free" in p["diet"]
        assert "breakfast" in p["meals"]
        assert p["price_usd"] < 5
        assert p["stock"] > 0
        assert p["name"] in result["answer"]


def test_ask_nothing_found(services):
    result = services.asker.ask("vegan zzzzqqq")
    assert result["products"] == []
    assert "could not find" in result["answer"]
