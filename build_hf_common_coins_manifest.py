"""
Pull Ayodelesamuel1/UsCoinsCommon from Hugging Face (MIT licensed) to close
the coverage gap identified earlier: our reference set had zero examples of
the everyday Lincoln cents / Jefferson nickels / Washington quarters that
actually fill the user's bag. Per user's choice, the raw images stay in the
local HF cache (not committed) - only the resulting embeddings get committed.
This manifest is the local-only bridge between the two; regenerate it with
this script on any machine that needs to rebuild training_embeddings.npz
from scratch.
"""
import csv

from huggingface_hub import snapshot_download

REPO_ID = "Ayodelesamuel1/UsCoinsCommon"
OUT_PATH = "hf_common_coins_manifest.csv"
FIELDS = ["file", "source_type", "class_label", "denomination", "year", "confidence", "notes"]

FOLDER_INFO = {
    "Jefferson Nickels, 1938-Date": dict(
        series="Jefferson Nickel", denomination="Nickel (5 cents)", year="1938-present",
    ),
    "Lincoln Cents, 1909-Date": dict(
        series="Lincoln Cent", denomination="Cent", year="1909-present",
    ),
    "Washington Quarters, 1932-1998": dict(
        series="Washington Quarter", denomination="Quarter", year="1932-1998",
    ),
}


def build():
    print(f"Downloading/verifying local cache for {REPO_ID}...")
    snapshot_dir = snapshot_download(REPO_ID, repo_type="dataset")

    import os
    rows = []
    for folder, info in FOLDER_INFO.items():
        folder_path = os.path.join(snapshot_dir, folder)
        if not os.path.isdir(folder_path):
            print(f"  missing folder: {folder}")
            continue
        for fname in sorted(os.listdir(folder_path)):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            low = fname.lower()
            if "obverse" in low:
                side = "obverse"
            elif "reverse" in low:
                side = "reverse"
            else:
                # Side-less images (an older, messier naming batch - all Washington
                # quarters) proved to be nearest-neighbor "generic silver disc"
                # attractors that dragged held-out accuracy down (42%->45% when
                # dropped, with no class regressing). Skip them.
                continue
            rows.append({
                "file": os.path.join(folder_path, fname),
                "source_type": "hf_common_coins",
                "class_label": f"{info['series']} ({side})",
                "denomination": info["denomination"],
                "year": info["year"],
                "confidence": "medium",
                "notes": f"From Hugging Face dataset {REPO_ID} (MIT license) - folder-level era only, no per-image date.",
            })

    with open(OUT_PATH, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUT_PATH}")
    by_folder = {}
    for folder, info in FOLDER_INFO.items():
        by_folder[info["series"]] = sum(1 for r in rows if r["class_label"].startswith(info["series"]))
    for series, count in by_folder.items():
        print(f"  {series}: {count}")


if __name__ == "__main__":
    build()
