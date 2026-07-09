import csv

from coin_inventory_data import INVENTORY
from training_labels import LABELS as FS_LABELS
from training_labels_named import NAMED_LABELS, SERIES_LABELS

OUT_PATH = "training_manifest.csv"
FIELDS = ["file", "source_type", "class_label", "denomination", "year", "confidence", "notes"]


def build():
    rows = []

    for r in SERIES_LABELS:
        rows.append({
            "file": f"training/{r['file']}", "source_type": "series_reference",
            "class_label": f"{r['series']} {r['denomination']}",
            "denomination": r["denomination"], "year": r["years"],
            "confidence": "high", "notes": "One reference image per design era - not a single date.",
        })

    for r in NAMED_LABELS:
        rows.append({
            "file": f"training/{r['file']}", "source_type": "named_reference",
            "class_label": f"{r['series']} ({r['side']})",
            "denomination": "bullion/proof/commemorative product", "year": r["year"] or "",
            "confidence": "high", "notes": "",
        })

    for r in FS_LABELS:
        rows.append({
            "file": f"training/{r['file']}", "source_type": "fs_auction_photo",
            "class_label": f"{r['series']} {r['denomination']}",
            "denomination": r["denomination"], "year": r["year"] or "",
            "confidence": r["confidence"], "notes": r["notes"],
        })

    skipped = 0
    for r in INVENTORY:
        crop = r.get("crop_file")
        if not crop:
            continue
        path = f"coin_crops/{crop}"
        rows.append({
            "file": path, "source_type": "user_collection_crop",
            "class_label": r["design_variety"],
            "denomination": r["category"], "year": r["year"] or "",
            "confidence": r["confidence"], "notes": r.get("notes", ""),
        })

    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    print(f"  series_reference:   {len(SERIES_LABELS)}")
    print(f"  named_reference:    {len(NAMED_LABELS)}")
    print(f"  fs_auction_photo:   {len(FS_LABELS)}")
    print(f"  user_collection_crop: {len(rows) - len(SERIES_LABELS) - len(NAMED_LABELS) - len(FS_LABELS)}")

    class_counts = {}
    for r in rows:
        class_counts[r["class_label"]] = class_counts.get(r["class_label"], 0) + 1
    single_image_classes = sum(1 for c in class_counts.values() if c == 1)
    print(f"  distinct class labels: {len(class_counts)}")
    print(f"  classes with only 1 image: {single_image_classes}")


if __name__ == "__main__":
    build()
