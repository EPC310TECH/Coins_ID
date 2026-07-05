import csv
import html
import os

from PIL import Image

CSV_PATH = "coin_inventory.csv"
IMAGES_DIR = "coin_images"
THUMBS_DIR = "report_thumbs"
OUT_PATH = "report.html"
THUMB_WIDTH = 320


def make_thumb(image_name):
    src = os.path.join(IMAGES_DIR, image_name)
    if not os.path.exists(src):
        return None
    os.makedirs(THUMBS_DIR, exist_ok=True)
    dst = os.path.join(THUMBS_DIR, image_name)
    if not os.path.exists(dst):
        img = Image.open(src)
        img = img.convert("RGB")
        ratio = THUMB_WIDTH / img.width
        img = img.resize((THUMB_WIDTH, int(img.height * ratio)), Image.LANCZOS)
        # normalize orientation-heavy portrait shots to a sane max height
        img.save(dst, quality=85)
    return dst


def first_image(source_images_field):
    first = source_images_field.split(",")[0].strip()
    return first + ".jpeg" if not first.lower().endswith(".jpeg") else first


def fmt_money(row, low_key, high_key):
    low, high = row[low_key], row[high_key]
    try:
        low_f, high_f = float(low), float(high)
    except ValueError:
        return html.escape(f"{low}-{high}")
    if low_f == high_f:
        return f"${low_f:,.2f}"
    return f"${low_f:,.2f} - ${high_f:,.2f}"


CATEGORY_ORDER = [
    "Proof Set", "Mint Set", "Commemorative Display Card",
    "Casino Token", "Elongated Cent (souvenir)",
    "Circulating Quarter", "Circulating Dime", "Circulating Nickel",
    "Circulating Cent (individually read)",
    "Circulating Cent (bulk, unread)",
    "Circulating Cent (bulk, possible duplicate photos)",
]


def category_rank(cat):
    return CATEGORY_ORDER.index(cat) if cat in CATEGORY_ORDER else len(CATEGORY_ORDER)


def build():
    with open(CSV_PATH, newline="") as f:
        rows = list(csv.DictReader(f))

    rows.sort(key=lambda r: category_rank(r["category"]))

    total_low = sum(float(r["est_value_low_usd"]) * float(r["qty"] or 1) for r in rows)
    total_high = sum(float(r["est_value_high_usd"]) * float(r["qty"] or 1) for r in rows)
    total_coins = sum(int(float(r["qty"] or 1)) for r in rows)

    parts = [
        """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Coin Collection Inventory</title>
<style>
  body { font-family: -apple-system, Segoe UI, Roboto, sans-serif; margin: 0; padding: 0 0 4rem; background: #f4f2ee; color: #222; }
  header { background: #1c2b3a; color: #fff; padding: 2rem; }
  header h1 { margin: 0 0 .3rem; font-size: 1.6rem; }
  header p { margin: 0; opacity: .85; }
  .summary { display: flex; gap: 2rem; padding: 1.2rem 2rem; background: #26374a; color: #fff; flex-wrap: wrap; }
  .summary div b { display: block; font-size: 1.4rem; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 1.1rem; padding: 1.5rem 2rem; }
  .card { background: #fff; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,.12); overflow: hidden; display: flex; flex-direction: column; }
  .card img { width: 100%; display: block; background: #ddd; }
  .card .body { padding: .9rem 1rem 1.1rem; flex: 1; display: flex; flex-direction: column; gap: .35rem; }
  .card h3 { margin: 0; font-size: 1.02rem; }
  .tag { display: inline-block; font-size: .68rem; text-transform: uppercase; letter-spacing: .04em; background: #eef1f5; color: #445; padding: .15rem .5rem; border-radius: 999px; margin-right: .3rem; }
  .value { font-weight: 600; color: #1a6b3c; }
  .conf-low { color: #a25b00; }
  .conf-medium { color: #7a6a00; }
  .conf-high { color: #1a6b3c; }
  .field { font-size: .84rem; line-height: 1.35; }
  .field b { color: #555; }
  .notes { font-size: .8rem; background: #fbf6e6; border-left: 3px solid #e0c46a; padding: .5rem .6rem; margin-top: .3rem; }
  h2.section { margin: 2rem 2rem 0; font-size: 1.15rem; color: #1c2b3a; border-bottom: 2px solid #1c2b3a; padding-bottom: .3rem; }
</style>
</head>
<body>
<header>
  <h1>Coin Collection Inventory</h1>
  <p>Identified from photos in coin_images/ - estimated values are reference-guide ranges for common circulated/typical grade examples, not appraisals. Grade-sensitive items need an in-hand look or certified grading.</p>
</header>
<div class="summary">
  <div><b>"""
        + str(len(rows))
        + """</b>catalog rows</div>
  <div><b>"""
        + str(total_coins)
        + """</b>coins/items covered</div>
  <div><b>$"""
        + f"{total_low:,.2f} - ${total_high:,.2f}"
        + """</b>estimated total value range</div>
</div>
<div class="grid">
"""
    ]

    current_cat = None
    for row in rows:
        if row["category"] != current_cat:
            current_cat = row["category"]
            parts.append(f'</div><h2 class="section">{html.escape(current_cat)}</h2><div class="grid">')

        img_name = first_image(row["source_images"])
        thumb = make_thumb(img_name)
        img_tag = (
            f'<img src="{THUMBS_DIR}/{html.escape(img_name)}" alt="{html.escape(img_name)}">'
            if thumb else '<div style="height:180px;background:#ddd"></div>'
        )

        value_str = fmt_money(row, "est_value_low_usd", "est_value_high_usd")
        conf_class = f"conf-{row['confidence']}" if row["confidence"] in ("low", "medium", "high") else ""

        specs = " / ".join(
            filter(None, [
                f"{row['diameter_mm']}mm" if row["diameter_mm"] else "",
                f"{row['weight_g']}g" if row["weight_g"] else "",
                row["composition"],
            ])
        )

        parts.append(f"""
  <div class="card">
    {img_tag}
    <div class="body">
      <h3>{html.escape(row['design_variety'])}</h3>
      <div>
        <span class="tag">{html.escape(str(row['year']) if row['year'] else 'undated')}</span>
        <span class="tag">qty {html.escape(row['qty'])}</span>
        <span class="tag {conf_class}">confidence: {html.escape(row['confidence'])}</span>
      </div>
      <div class="field"><b>Value:</b> <span class="value">{value_str}</span> - {html.escape(row['value_basis'])}</div>
      <div class="field"><b>Specs:</b> {html.escape(specs) if specs else 'n/a'}</div>
      <div class="field"><b>Obverse:</b> {html.escape(row['obverse_text'])}</div>
      <div class="field"><b>Reverse:</b> {html.escape(row['reverse_text'])}</div>
      <div class="field"><b>Condition:</b> {html.escape(row['condition_notes'])}</div>
      <div class="field"><b>Source photo(s):</b> {html.escape(row['source_images'])}</div>
      {f'<div class="notes">{html.escape(row["notes"])}</div>' if row['notes'] else ''}
    </div>
  </div>
""")

    parts.append("</div></body></html>")

    with open(OUT_PATH, "w") as f:
        f.write("".join(parts))
    print(f"Wrote {OUT_PATH} ({len(rows)} cards)")


if __name__ == "__main__":
    build()
