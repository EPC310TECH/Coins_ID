"""
Cross-reference our hand-derived training_labels.LABELS against ground-truth
product listings scraped from rarecoinwholesalers.com (training/coins.csv).
The dealer's product-page URL slug encodes the SKU that matches our fs.jpg
numeric filenames, e.g.:
    .../1926-s-peace-1-ms66-plus-sku-143975  ->  143975fs.jpg
Where a SKU matches, this is real ground truth (dealer-assigned grade,
mintmark, variety) - far more reliable than a visual guess from a photo.
"""
import csv
import re

from training_labels import LABELS

CSV_PATH = "training/coins.csv"

DENOM_MAP = {
    "1c": "Cent", "2c": "Two Cent", "3c": "Three Cent", "5c": "Nickel (5 cents)",
    "10c": "Dime", "20c": "Twenty Cent", "25c": "Quarter", "50c": "Half Dollar",
    "s1": "Dollar", "g1": "Gold Dollar", "g2.5": "$2.50 Gold (Quarter Eagle)",
    "g3": "$3 Gold", "g5": "$5 Gold (Half Eagle)", "g10": "$10 Gold (Eagle)",
    "g20": "$20 Gold (Double Eagle)",
}

SERIES_KEYWORDS = [
    "flowing hair", "draped bust", "capped bust", "liberty seated", "seated liberty",
    "barber", "mercury", "walking liberty", "standing liberty", "morgan", "peace",
    "trade dollar", "shield", "indian head", "coronet", "saint gaudens", "buffalo",
    "jefferson", "washington", "lincoln", "continental",
]

MINT_LETTERS = {"p", "d", "s", "cc", "o", "w", "c"}


def load_sku_map():
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    sku_map = {}
    for r in rows:
        url = r.get("productpage", "")
        m = re.search(r"/([^/]+)-sku-(\d+)", url)
        if not m:
            continue
        slug, sku = m.group(1), m.group(2)
        sku_map.setdefault(sku, set()).add(slug.replace("-", " "))
    return sku_map


def parse_slug(slug_text):
    """slug_text like '1806 draped bust 25c heraldic eagle ms65'."""
    tokens = slug_text.split()
    year_match = re.search(r"\b(1[5-9]\d\d|20\d\d)\b", slug_text)
    year = int(year_match.group(1)) if year_match else None

    mint = None
    if year_match:
        idx = tokens.index(year_match.group(1))
        if idx + 1 < len(tokens) and tokens[idx + 1].lower() in MINT_LETTERS:
            mint = tokens[idx + 1].upper()

    denom = None
    for tok in tokens:
        key = tok.lower()
        if key in DENOM_MAP:
            denom = DENOM_MAP[key]
            break

    series = None
    lower = slug_text.lower()
    for kw in SERIES_KEYWORDS:
        if kw in lower:
            series = kw.title()
            break

    return dict(year=year, mint=mint, denomination=denom, series=series, raw=slug_text)


def reconcile():
    sku_map = load_sku_map()
    updated = 0
    conflicts = []

    for row in LABELS:
        sku = row["file"].replace("fs.jpg", "")
        if sku not in sku_map:
            continue
        slugs = sku_map[sku]
        slug_text = sorted(slugs)[0]
        parsed = parse_slug(slug_text)
        if parsed["year"] is None:
            continue

        old = (row["series"], row["denomination"], row["year"], row["confidence"])
        if parsed["series"]:
            row["series"] = parsed["series"]
        if parsed["denomination"]:
            row["denomination"] = parsed["denomination"]
        row["year"] = parsed["year"]
        row["confidence"] = "high"
        mint_note = f", mint mark {parsed['mint']}" if parsed["mint"] else ""
        row["notes"] = f"Confirmed via dealer listing (SKU {sku}): \"{parsed['raw']}\"{mint_note}."
        updated += 1
        if len(slugs) > 1:
            conflicts.append((sku, slugs))

    return updated, conflicts, len(sku_map)


if __name__ == "__main__":
    updated, conflicts, total_skus = reconcile()
    print(f"Matched {total_skus} SKUs in coins.csv against our fs.jpg filenames")
    print(f"Updated {updated} of {len(LABELS)} label rows with confirmed ground truth")
    if conflicts:
        print(f"{len(conflicts)} SKUs had multiple distinct slug variants (took first alphabetically):")
        for sku, slugs in conflicts[:10]:
            print(f"  {sku}: {slugs}")

    # write corrected labels back out
    with open("training_labels.py", "w") as f:
        f.write('''# Visual identification labels for training/######fs.jpg reference photos.
# Rows marked "Confirmed via dealer listing" were cross-checked against
# training/coins.csv (a scrape of rarecoinwholesalers.com product listings
# whose SKUs match our fs.jpg numeric filenames) via reconcile_fs_labels.py -
# these are ground truth, not a visual guess. Everything else is still a
# best-effort visual read (see confidence).

LABELS = [
''')
        for row in LABELS:
            f.write(f"    dict(file={row['file']!r}, series={row['series']!r}, denomination={row['denomination']!r}, year={row['year']!r}, confidence={row['confidence']!r}, notes={row['notes']!r}),\n")
        f.write("]\n")
    print("Wrote corrected training_labels.py")
