"""
Pull four mid-20th-century circulating US coin types from the Kaggle dataset
jaronfralick/rare-us-coin-image-dataset (MIT) to close a gap in the reference
set: Eisenhower dollars, Franklin & Kennedy half dollars, and Susan B. Anthony
dollars had zero examples. Morgan dollars are already covered by SERIES_LABELS
in training_labels_named.py, so that folder is intentionally skipped.

Provenance caveat: per the dataset author these images are screenshots scraped
from coin-vendor sites, so confidence is "medium" and they are labeled as
ordinary circulating types, NOT rare/key-date candidates (see rare_flags.py).

Like the HF common-coins bridge (build_hf_common_coins_manifest.py), the raw
images stay in a local cache (~/.cache/kaggle_coin_datasets/, not committed);
only the resulting embeddings get committed. Regenerate this manifest with this
script before rebuilding training_embeddings.npz on a fresh machine. Download
the archive first via the Kaggle MCP `download_dataset` signed URL and extract
the four *_All folders into CACHE_DIR.
"""
import csv
import os

OUT_PATH = "rare_us_coins_manifest.csv"
FIELDS = ["file", "source_type", "class_label", "denomination", "year", "confidence", "notes"]

DATASET = "jaronfralick/rare-us-coin-image-dataset"
CACHE_DIR = os.path.expanduser(
    "~/.cache/kaggle_coin_datasets/rare-us-coin-image-dataset/base_data_RUSCoinNet"
)

# Morgan_All is deliberately omitted - already covered by SERIES_LABELS.
FOLDER_INFO = {
    "Eisenhower_All": dict(class_label="Eisenhower Dollar", denomination="Dollar", year="1971-1978"),
    "Franklin_All":   dict(class_label="Franklin Half Dollar", denomination="Half Dollar", year="1948-1963"),
    "Kennedy_All":    dict(class_label="Kennedy Half Dollar", denomination="Half Dollar", year="1964-present"),
    "Susan_All":      dict(class_label="Susan B. Anthony Dollar", denomination="Dollar", year="1979-1981, 1999"),
}


def build():
    rows = []
    for folder, info in FOLDER_INFO.items():
        folder_path = os.path.join(CACHE_DIR, folder)
        if not os.path.isdir(folder_path):
            print(f"  missing folder (run the download/extract first): {folder_path}")
            continue
        for fname in sorted(os.listdir(folder_path)):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            rows.append({
                "file": os.path.join(folder_path, fname),
                "source_type": "kaggle_rare_us_coins",
                "class_label": info["class_label"],
                "denomination": info["denomination"],
                "year": info["year"],
                "confidence": "medium",
                "notes": (
                    f"From Kaggle dataset {DATASET} (MIT license) - scraped vendor "
                    "screenshots, folder-level type only, no per-image date or side. "
                    "Common circulating type, NOT a rare/key-date flag."
                ),
            })

    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    for info in FOLDER_INFO.values():
        count = sum(1 for r in rows if r["class_label"] == info["class_label"])
        print(f"  {info['class_label']}: {count}")


if __name__ == "__main__":
    build()
