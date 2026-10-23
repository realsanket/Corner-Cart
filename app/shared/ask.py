"""Ask the shop, local mode: keyword search plus simple filters read from the text.

"something gluten-free for breakfast under $5" becomes: diet = gluten-free, meal = breakfast,
price < 5.00, nothing left over to match as a word. No model, no embeddings: that is the point of
keyword mode, and what the M2 labs replace with search by meaning.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

DIET_PATTERNS = {
    "gluten-free": r"gluten[\s-]*free|no gluten|without gluten|coeliac|celiac",
    "vegan": r"vegan|plant[\s-]*based",
    "sugar-free": r"sugar[\s-]*free|no (?:added )?sugar|without sugar",
    "nut-free": r"nut[\s-]*free|no nuts|without nuts",
}
MEAL_WORDS = {
    "breakfast": "breakfast", "lunch": "lunch", "dinner": "dinner", "supper": "dinner",
    "snack": "snack", "snacks": "snack",
}  # fmt: skip
PRICE_PATTERNS = [  # (regex, inclusive)
    (r"(?:under|below|less than|cheaper than|beneath)\s*(?:us)?\$?\s*(\d+(?:\.\d+)?)", False),
    (r"(?:up to|at most|no more than|max(?:imum)?(?: of)?|within)\s*(?:us)?\$?\s*(\d+(?:\.\d+)?)", True),
    (r"<\s*=?\s*\$?\s*(\d+(?:\.\d+)?)", False),
    (r"(\d+(?:\.\d+)?)\s*(?:dollars|usd|bucks)\s*or\s*(?:less|under)", True),
]  # fmt: skip
STOPWORDS = set("""a an and any are as at be by can could do find for from get give good have i in is it
me my need needs of on one or please show some something the there to want what which with would you
under below less than cheaper dollars dollar usd bucks something anything something""".split())


@dataclass
class Query:
    text: str
    diets: list[str] = field(default_factory=list)
    meals: list[str] = field(default_factory=list)
    max_price: float | None = None
    price_inclusive: bool = False
    words: list[str] = field(default_factory=list)

    def filters_text(self) -> str:
        parts = list(self.diets) + list(self.meals)
        if self.max_price is not None:
            parts.append(f"{'up to' if self.price_inclusive else 'under'} ${self.max_price:g}")
        return ", ".join(parts)


def _stem(word: str) -> str:
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def parse_query(text: str) -> Query:
    q = Query(text=text.strip())
    rest = text.lower()
    for diet, pattern in DIET_PATTERNS.items():
        if re.search(pattern, rest):
            q.diets.append(diet)
            rest = re.sub(pattern, " ", rest)
    for pattern, inclusive in PRICE_PATTERNS:
        m = re.search(pattern, rest)
        if m:
            q.max_price, q.price_inclusive = float(m.group(1)), inclusive
            rest = rest.replace(m.group(0), " ")
            break
    for raw in re.findall(r"[a-z][a-z'-]*", rest):
        if raw in MEAL_WORDS:
            if MEAL_WORDS[raw] not in q.meals:
                q.meals.append(MEAL_WORDS[raw])
        elif raw not in STOPWORDS and len(raw) > 1:
            q.words.append(_stem(raw))
    return q


def _matches_filters(p: dict, q: Query) -> bool:
    if any(d not in p["diet"] for d in q.diets):
        return False
    if q.max_price is not None:
        if p["price_usd"] > q.max_price or (not q.price_inclusive and p["price_usd"] >= q.max_price):
            return False
    return True


def _score(p: dict, q: Query) -> int:
    name = p["name"].lower()
    category = p["category"].lower()
    note = p["note"].lower()
    score = 0
    for w in q.words:
        if w in name:
            score += 4
        if w in category:
            score += 2
        if w in note:
            score += 1
    for meal in q.meals:
        if meal in p["meals"]:
            score += 4
        if meal in category:
            score += 3
    return score


def search(products: list[dict], q: Query, ratings: dict[str, float] | None = None, limit: int = 20,
           one_per_family: bool = False) -> list[dict]:  # fmt: skip
    """Products matching the filters, best keyword match first, then best rated, then cheapest."""
    ratings = ratings or {}
    has_terms = bool(q.words or q.meals)
    scored = []
    for p in products:
        if p["stock"] <= 0 or not _matches_filters(p, q):
            continue
        s = _score(p, q)
        if has_terms and s == 0:
            continue
        scored.append((-s, -ratings.get(p["id"], 0.0), p["price_usd"], p["id"], p))
    scored.sort(key=lambda t: t[:4])
    out, seen = [], set()
    for *_, p in scored:
        if one_per_family:
            if p["family"] in seen:
                continue
            seen.add(p["family"])
        out.append(p)
        if len(out) == limit:
            break
    return out


def _join(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def answer_sentence(q: Query, hits: list[dict]) -> str:
    """One templated sentence that names the products. Keyword mode: no model wrote this."""
    if not hits:
        extra = f" with {q.filters_text()}" if q.filters_text() else ""
        return f"I could not find anything{extra} for that. Try fewer words or a different filter."
    named = [f"{p['name']} ({p['pack']}, ${p['price_usd']:.2f})" for p in hits]
    verb = "is" if len(hits) == 1 else "are"
    tail = f" All {verb} " if len(hits) > 1 else " It is "
    labels = [d for d in q.diets]
    if q.max_price is not None:
        labels.append(f"{'up to' if q.price_inclusive else 'under'} ${q.max_price:g}")
    suffix = tail + _join(labels) + "." if labels else ""
    lead = "Here is a match" if len(hits) == 1 else f"Here are {len(hits)} matches"
    meal = f" for {_join(q.meals)}" if q.meals else ""
    return f"{lead}{meal}: {_join(named)}.{suffix}"


def ask(products: list[dict], text: str, ratings: dict[str, float] | None = None, top: int = 3) -> dict:
    q = parse_query(text)
    hits = search(products, q, ratings, limit=top, one_per_family=True)
    return {
        "mode": "keyword",
        "question": q.text,
        "filters": {"diet": q.diets, "meal": q.meals, "max_price_usd": q.max_price,
                    "keywords": q.words},  # fmt: skip
        "answer": answer_sentence(q, hits),
        "products": hits,
    }
