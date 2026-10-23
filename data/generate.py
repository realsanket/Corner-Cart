#!/usr/bin/env python
"""Generate CornerCart's demo data with ONE fixed seed. Everything here is invented demo data.

    python data/generate.py                 # products, customers, reviews, orders, shop guide  (small, committed)
    python data/generate.py --price-history # also data/price_history.csv: ~365,000 rows, NOT committed

The same seed always gives byte-identical files. No wall clock, no global random state.
Money is US dollars, packs are metric, times are UTC.
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog_seed import BASES, FOOD_QUALIFIERS, HOME_QUALIFIERS, PACKS  # noqa: E402
from guide_pages import GUIDE  # noqa: E402

SEED = 20261023
DATA_DIR = Path(__file__).resolve().parent
N_PRODUCTS = 1000
N_CUSTOMERS = 200
N_REVIEWS = 3000
N_ORDERS = 300
PRICE_DAYS = 365
LABEL = "demo data: invented for the CornerCart lessons"

# The "today" of the demo world: fixed, so the files never change from one run to the next.
WORLD_END = datetime(2026, 10, 1, tzinfo=UTC)

TAGS = {"g": "gluten-free", "v": "vegan", "s": "sugar-free", "n": "nut-free"}
MEALS = {"b": "breakfast", "l": "lunch", "d": "dinner", "s": "snack"}
CATEGORY_ORDER = [
    "Dairy & Eggs", "Bakery", "Breakfast", "Fruit", "Vegetables", "Rice, Pasta & Grains",
    "Pantry", "Coffee & Tea", "Snacks", "Drinks", "Frozen", "Cleaning & Household",
]  # fmt: skip
# Pack sets that read oddly with a few qualifiers ("Concentrated Bin Bags")
SIMPLE_HOME_PACKS = {"BAG", "ROLL", "FOIL", "SPG", "WIPE", "TAB", "U4"}
SIMPLE_HOME_QUALIFIERS = {"Eco", "Value", "Family Size", "Everyday", "Heavy Duty", "Classic"}

FIRST_NAMES = """Amara Wei Priya Mateo Fatima Kenji Olga Kwame Sofia Liam Noor Hiro Aisha Lars Chidi Mei Diego Ananya
Yusuf Ingrid Thabo Camila Dmitri Elif Jin Zainab Pablo Naledi Ravi Sakura Omar Freya Arjun Lucia Tariq Hana Mohammed
Isabel Kofi Yuki Nia Santiago Leila Anders Chloe Rohan Adaeze Mina Emre Tomas Layla Bao Marta Sipho Ayesha Felix
Daniela Haruto Mariam Pedro Anika Joon Rania Ivan Esther Kavya Hugo Salma Jamal Eva Takumi Zola Nikolai Imani Carmen
Abebe Siti Noah Dalia Raj Malia Stefan Yara Ali Greta Chen Tunde Ximena Bilal Aroha""".split()
LAST_NAMES = """Okafor Tanaka Singh Garcia Haddad Kim Novak Mensah Rossi Nguyen Silva Cohen Ivanov Lindgren Abdi Patel
Kowalski Mwangi Yilmaz Suzuki Fernandez Hassan Larsen Chowdhury Oliveira Santos Dubois Schmidt Park Banerjee Nasser
Moreno Zhang Eze Johansson Rahman Costa Petrov Wong Ibrahim Alvarez Khan Sato Mbeki Romero Lopez Bianchi Das Aziz
Wilson Murphy Hoang Obi Pereira Berg Takahashi Sharma Said Mutua Reyes Ahmed Varga Torres Yamamoto Naidoo Fraser
Demir Gupta Zulu Ortiz Lund Chaudhry Ali Barros Kone Walker""".split()
CITIES = [
    ("Lagos", "Nigeria"), ("Nairobi", "Kenya"), ("Cape Town", "South Africa"), ("Accra", "Ghana"),
    ("Cairo", "Egypt"), ("Casablanca", "Morocco"), ("Mumbai", "India"), ("Bengaluru", "India"),
    ("Dhaka", "Bangladesh"), ("Karachi", "Pakistan"), ("Colombo", "Sri Lanka"), ("Jakarta", "Indonesia"),
    ("Manila", "Philippines"), ("Hanoi", "Vietnam"), ("Bangkok", "Thailand"), ("Singapore", "Singapore"),
    ("Seoul", "South Korea"), ("Tokyo", "Japan"), ("Osaka", "Japan"), ("Shanghai", "China"),
    ("Sydney", "Australia"), ("Auckland", "New Zealand"), ("Dubai", "United Arab Emirates"),
    ("Istanbul", "Turkey"), ("Riyadh", "Saudi Arabia"), ("Athens", "Greece"), ("Rome", "Italy"),
    ("Madrid", "Spain"), ("Lisbon", "Portugal"), ("Paris", "France"), ("Berlin", "Germany"),
    ("Warsaw", "Poland"), ("Stockholm", "Sweden"), ("Dublin", "Ireland"), ("London", "United Kingdom"),
    ("Toronto", "Canada"), ("Chicago", "United States"), ("Austin", "United States"),
    ("Mexico City", "Mexico"), ("Bogota", "Colombia"), ("Lima", "Peru"), ("Santiago", "Chile"),
    ("Sao Paulo", "Brazil"), ("Buenos Aires", "Argentina"),
]  # fmt: skip

REVIEW_OPENERS = {
    5: ["Absolutely love this.", "Excellent, will buy again.", "Perfect, exactly what I wanted.",
        "Great quality and great value.", "My family asks for this every week.", "Five stars from me.",
        "Better than I expected.", "A real favourite in our house."],
    4: ["Really good.", "Very happy with this.", "Good quality for the price.", "Solid choice.",
        "Nearly perfect.", "Would recommend.", "Does the job nicely.", "A reliable pick."],
    3: ["It is fine.", "Average, nothing special.", "Okay for the price.", "Does what it says.",
        "Decent but not amazing.", "Good enough for every day."],
    2: ["A bit disappointing.", "Not as good as I hoped.", "Below what I expected.",
        "Would not buy again.", "Quality was patchy."],
    1: ["Very disappointed.", "Not good at all.", "Poor quality.", "I would not recommend this.",
        "Arrived in bad shape."],
}  # fmt: skip
FOOD_DETAILS = [
    "The {pack} size lasts us about a week.", "Fresh and tasty, and it arrived well packed.",
    "Good flavour, and the {pack} pack is the right size.", "The kids eat it without complaining.",
    "Easy to store and it keeps well.", "The best {name} I have bought online.",
    "Great with breakfast.", "Fine for cooking dinner for the family.",
    "Tastes the way I remember it from home.", "Fair price for the {pack} pack.",
    "Use-by date was far away, which I liked.", "Delivery was quick and everything was cold.",
]  # fmt: skip
HOME_DETAILS = [
    "Works well and the {pack} pack lasts a long time.", "Does the job without leaving marks.",
    "The smell is pleasant but not too strong.", "Good value for the {pack} pack.",
    "Arrived well packed.", "Easy to use, and I will order {name} again.",
    "Strong enough for the kitchen and gentle on hands.", "A little goes a long way.",
]  # fmt: skip

SHOP_STATUSES = ["placed", "packed", "invoiced"]


def _price(rng: random.Random, value: float) -> float:
    """Round to a shop-looking price: ends in .x9 or .x5 (or .00 for round numbers)."""
    cents = round(value * 100)
    ending = rng.choice([9, 9, 9, 5, 5, 0])
    cents = max(29, (cents // 10) * 10 + ending)
    return round(cents / 100, 2)


def build_products(rng: random.Random) -> list[dict]:
    """~1,000 everyday groceries: every base item times a handful of qualifiers, sampled to exactly 1,000."""
    combos = []  # (base_index, qualifier_index)
    parsed = []
    for line in BASES:
        category, name, packs, price, tags, meals, note = (p.strip() for p in line.split("|"))
        home = category == "Cleaning & Household"
        quals = HOME_QUALIFIERS if home else FOOD_QUALIFIERS
        if home and packs in SIMPLE_HOME_PACKS:
            quals = [q for q in quals if q[0] in SIMPLE_HOME_QUALIFIERS]
        parsed.append(
            {"category": category, "name": name, "packs": PACKS[packs], "price": float(price),
             "tags": [TAGS[c] for c in tags], "meals": [MEALS[c] for c in meals], "note": note,
             "quals": quals}
        )  # fmt: skip
    # every base item gets at least two variants, the rest are sampled from what is left
    rest = []
    for bi, b in enumerate(parsed):
        order = list(range(len(b["quals"])))
        rng.shuffle(order)
        combos += [(bi, qi) for qi in order[:2]]
        rest += [(bi, qi) for qi in order[2:]]
    rng.shuffle(rest)
    combos += rest[: N_PRODUCTS - len(combos)]
    if len(combos) < N_PRODUCTS:
        raise SystemExit(f"catalog_seed.py has too few combinations ({len(combos)})")
    combos.sort(key=lambda c: (CATEGORY_ORDER.index(parsed[c[0]]["category"]), c[0], c[1]))

    products = []
    for n, (bi, qi) in enumerate(combos, start=1):
        b = parsed[bi]
        word, factor, pack_pick, sentence = b["quals"][qi]
        packs = b["packs"]
        if pack_pick == "small":
            pack, pf = packs[0]
        elif pack_pick == "large":
            pack, pf = packs[-1]
        elif pack_pick == "mid":
            pack, pf = packs[len(packs) // 2]
        else:
            pack, pf = rng.choice(packs)
        price = _price(rng, b["price"] * pf * factor * rng.uniform(0.92, 1.1))
        r = rng.random()
        stock = 0 if r < 0.04 else rng.randint(1, 9) if r < 0.12 else rng.randint(10, 400)
        products.append(
            {
                "id": f"p{n:04d}",
                "name": f"{word} {b['name']}",
                "family": b["name"],
                "category": b["category"],
                "price_usd": price,
                "pack": pack,
                "stock": stock,
                "diet": list(b["tags"]),
                "meals": list(b["meals"]),
                "note": f"{b['note']} {sentence}",
            }
        )
    return products


def build_customers(rng: random.Random) -> list[dict]:
    customers, seen = [], set()
    while len(customers) < N_CUSTOMERS:
        name = f"{rng.choice(FIRST_NAMES)} {rng.choice(LAST_NAMES)}"
        if name in seen:
            continue
        seen.add(name)
        city, country = rng.choice(CITIES)
        joined = WORLD_END - timedelta(days=rng.randint(30, 900))
        customers.append(
            {
                "id": f"c{len(customers) + 1:04d}",
                "name": name,
                "city": city,
                "country": country,
                "joined": joined.strftime("%Y-%m-%d"),
            }
        )
    return customers


def _iso(moment: datetime) -> str:
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def build_reviews(rng: random.Random, products: list[dict], customers: list[dict]) -> list[dict]:
    quality = {p["id"]: rng.uniform(3.0, 4.8) for p in products}  # some products are simply better liked
    start = WORLD_END - timedelta(days=330)
    raw = []
    for _ in range(N_REVIEWS):
        p = rng.choice(products)
        rating = int(min(5, max(1, round(rng.gauss(quality[p["id"]], 0.9)))))
        details = HOME_DETAILS if p["category"] == "Cleaning & Household" else FOOD_DETAILS
        opener = rng.choice(REVIEW_OPENERS[rating])
        detail = rng.choice(details).format(pack=p["pack"], name=p["family"].lower())
        text = f"{opener} {detail}"
        when = start + timedelta(seconds=rng.randint(0, 330 * 86400))
        raw.append((when, p["id"], rng.choice(customers)["id"], rating, text))
    raw.sort()
    return [
        {"id": f"r{i:05d}", "product_id": pid, "customer_id": cid, "rating": rating, "text": text,
         "created_at": _iso(when)}
        for i, (when, pid, cid, rating, text) in enumerate(raw, start=1)
    ]  # fmt: skip


def build_orders(rng: random.Random, products: list[dict], customers: list[dict]) -> list[dict]:
    in_stock = [p for p in products if p["stock"] > 0]
    start = WORLD_END - timedelta(days=60)
    raw = []
    for _ in range(N_ORDERS):
        when = start + timedelta(seconds=rng.randint(0, 60 * 86400))
        lines = []
        for p in rng.sample(in_stock, rng.randint(1, 6)):
            lines.append({"product_id": p["id"], "qty": rng.randint(1, 4), "unit_price_usd": p["price_usd"]})
        raw.append((when, rng.choice(customers)["id"], lines))
    raw.sort(key=lambda r: r[0])
    orders = []
    for i, (when, cid, lines) in enumerate(raw, start=1):
        age_days = (WORLD_END - when).days
        status = "invoiced" if age_days > 2 else rng.choice(SHOP_STATUSES)
        total = sum(round(line["qty"] * line["unit_price_usd"] * 100) for line in lines) / 100
        orders.append(
            {"id": f"o{i:05d}", "customer_id": cid, "status": status, "created_at": _iso(when),
             "lines": lines, "total_usd": round(total, 2)}
        )  # fmt: skip
    return orders


def iter_price_history(products: list[dict]) -> Iterator[tuple[str, str, float]]:
    """Daily price of every product for 365 days (365,000 rows for 1,000 products). Generated on demand."""
    first_day = WORLD_END - timedelta(days=PRICE_DAYS)
    for index, p in enumerate(products):
        rng = random.Random(SEED * 1000 + index)  # own stream per product: stable even if others change
        price = p["price_usd"] * rng.uniform(0.85, 1.0)
        for day in range(PRICE_DAYS):
            price *= 1 + rng.gauss(0.0004, 0.006)
            if rng.random() < 0.01:  # an occasional promotion
                shown = price * rng.uniform(0.75, 0.9)
            else:
                shown = price
            yield p["id"], (first_day + timedelta(days=day)).strftime("%Y-%m-%d"), round(max(0.25, shown), 2)


def build_all() -> dict[str, list[dict]]:
    """Everything small enough to commit, from the one seed."""
    rng = random.Random(SEED)
    products = build_products(rng)
    customers = build_customers(rng)
    reviews = build_reviews(rng, products, customers)
    orders = build_orders(rng, products, customers)
    return {"products": products, "customers": customers, "reviews": reviews, "orders": orders}


def dumps_records(records: list[dict]) -> str:
    """A JSON list with one record per line: small files, readable diffs."""
    return "[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n]\n"


def write_all(out_dir: Path = DATA_DIR) -> dict[str, int]:
    sizes = {}
    for name, records in build_all().items():
        path = out_dir / f"{name}.json"
        path.write_text(dumps_records(records), encoding="utf-8", newline="\n")
        sizes[path.name] = path.stat().st_size
    guide = out_dir / "shop-guide"
    guide.mkdir(exist_ok=True)
    for filename, text in GUIDE.items():
        (guide / filename).write_text(text, encoding="utf-8", newline="\n")
        sizes[f"shop-guide/{filename}"] = (guide / filename).stat().st_size
    return sizes


def write_price_history(out_dir: Path = DATA_DIR) -> int:
    products = build_all()["products"]
    path = out_dir / "price_history.csv"
    rows = 0
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["product_id", "date", "price_usd"])
        for row in iter_price_history(products):
            writer.writerow(row)
            rows += 1
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--price-history", action="store_true",
                        help="also write data/price_history.csv (not committed)")  # fmt: skip
    args = parser.parse_args()
    for name, size in write_all().items():
        print(f"wrote data/{name:<32} {size / 1024:8.1f} KB")
    if args.price_history:
        rows = write_price_history()
        print(f"wrote data/price_history.csv           {rows:,} rows")
    print(f"All {LABEL}. Seed {SEED}.")


if __name__ == "__main__":
    main()
