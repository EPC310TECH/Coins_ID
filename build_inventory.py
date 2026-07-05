import csv

from coin_inventory_data import INVENTORY
from coin_specs import COIN_SPECS

CSV_PATH = "coin_inventory.csv"

FIELDS = [
    "photo_group", "source_images", "category", "denomination", "country",
    "year", "mint_mark", "design_variety", "diameter_mm", "weight_g",
    "composition", "edge", "obverse_text", "reverse_text", "condition_notes",
    "qty", "est_value_low_usd", "est_value_high_usd", "value_basis",
    "confidence", "notes",
]


def spec_for(row):
    key = row.get("coin_spec_key")
    if not key:
        return {}
    # a couple of rows reference two spec keys separated by " / "; use the first
    first_key = key.split(" / ")[0].strip()
    return COIN_SPECS.get(first_key, {})


def build():
    with open(CSV_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in INVENTORY:
            spec = spec_for(row)
            out = {
                "photo_group": row["photo_group"],
                "source_images": row["source_images"],
                "category": row["category"],
                "denomination": row["denomination"],
                "country": row["country"],
                "year": row["year"],
                "mint_mark": row["mint_mark"],
                "design_variety": row["design_variety"],
                "diameter_mm": spec.get("diameter_mm", ""),
                "weight_g": spec.get("weight_g", ""),
                "composition": spec.get("composition", ""),
                "edge": spec.get("edge", ""),
                "obverse_text": row["obverse_text"],
                "reverse_text": row["reverse_text"],
                "condition_notes": row["condition_notes"],
                "qty": row["qty"],
                "est_value_low_usd": row["est_value_low_usd"],
                "est_value_high_usd": row["est_value_high_usd"],
                "value_basis": row["value_basis"],
                "confidence": row["confidence"],
                "notes": row["notes"],
            }
            writer.writerow(out)
    print(f"Wrote {len(INVENTORY)} rows to {CSV_PATH}")


if __name__ == "__main__":
    build()
