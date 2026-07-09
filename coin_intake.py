#!/usr/bin/env python3
"""
coin_intake.py — photo intake & renaming for coin inventory.

Workflow it expects (matches the slate-shot system):
  For each coin you shoot exactly N photos in order (default 3):
    1. slate  (coin next to its labeled flip so the ID is visible)
    2. obv    (obverse)
    3. rev    (reverse)
  Dump the whole card/folder of photos into INBOX, run this script.
  It walks them in capture order, groups every N into one coin,
  shows you the slate shot's filename/time, asks (or auto-assigns)
  the coin_id, renames into OUTBOX as:
      C0001-slate.jpg  C0001-obv.jpg  C0001-rev.jpg
  and appends a row to inventory.csv (and Supabase, if configured).

Usage:
  python coin_intake.py                    # interactive, prompts per coin
  python coin_intake.py --auto            # auto-assign next sequential IDs
  python coin_intake.py --start C0142     # begin auto numbering at C0142
  python coin_intake.py --shots 2         # 2 photos per coin (obv/rev, no slate)

Config via environment (optional Supabase sync):
  SUPABASE_URL, SUPABASE_SERVICE_KEY      # if unset, CSV-only mode
"""

import argparse
import csv
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ----------------------------------------------------------------
# Config — edit these paths to taste
# ----------------------------------------------------------------
INBOX = Path("./inbox")        # dump raw photos here
OUTBOX = Path("./photos")      # renamed photos land here
CSV_LOG = Path("./inventory.csv")

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff", ".webp", ".dng", ".cr2", ".nef", ".arw"}
ROLE_NAMES = {3: ["slate", "obv", "rev"], 2: ["obv", "rev"]}

CSV_FIELDS = [
    "coin_id", "photo_slate", "photo_obv", "photo_rev",
    "shot_time", "status", "created_at",
]

# ----------------------------------------------------------------


def capture_time(p: Path) -> float:
    """Best-effort capture time: EXIF if available, else file mtime."""
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        with Image.open(p) as img:
            exif = img.getexif()
            for tag_id, val in exif.items():
                if TAGS.get(tag_id) == "DateTimeOriginal":
                    return datetime.strptime(val, "%Y:%m:%d %H:%M:%S").timestamp()
    except Exception:
        pass
    return p.stat().st_mtime


def next_id_from_csv(csv_path: Path, prefix: str = "C") -> str:
    """Scan the CSV for the highest existing coin_id and return the next one."""
    highest = 0
    if csv_path.exists():
        with open(csv_path, newline="") as f:
            for row in csv.DictReader(f):
                m = re.fullmatch(rf"{prefix}(\d+)", row.get("coin_id", ""))
                if m:
                    highest = max(highest, int(m.group(1)))
    return f"{prefix}{highest + 1:04d}"


def bump_id(coin_id: str) -> str:
    m = re.fullmatch(r"([A-Za-z]+)(\d+)", coin_id)
    if not m:
        raise ValueError(f"Can't increment ID: {coin_id}")
    prefix, num = m.group(1), m.group(2)
    return f"{prefix}{int(num) + 1:0{len(num)}d}"


def append_csv(row: dict):
    new_file = not CSV_LOG.exists()
    with open(CSV_LOG, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        if new_file:
            w.writeheader()
        w.writerow(row)


def supabase_client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not (url and key):
        return None
    try:
        from supabase import create_client
        return create_client(url, key)
    except ImportError:
        print("  (supabase-py not installed; CSV-only. pip install supabase)")
        return None


def push_supabase(sb, row: dict):
    if sb is None:
        return
    try:
        sb.table("coins").upsert(
            {
                "coin_id": row["coin_id"],
                "photo_slate": row["photo_slate"] or None,
                "photo_obv": row["photo_obv"] or None,
                "photo_rev": row["photo_rev"] or None,
                "status": "photographed",
            },
            on_conflict="coin_id",
        ).execute()
    except Exception as e:
        print(f"  ⚠ Supabase sync failed for {row['coin_id']}: {e}")


def main():
    ap = argparse.ArgumentParser(description="Group, rename, and log coin photos.")
    ap.add_argument("--shots", type=int, default=3, choices=[2, 3],
                    help="photos per coin (3 = slate/obv/rev, 2 = obv/rev)")
    ap.add_argument("--auto", action="store_true",
                    help="auto-assign sequential IDs without prompting")
    ap.add_argument("--start", type=str, default=None,
                    help="starting coin_id for auto mode, e.g. C0142")
    ap.add_argument("--dry-run", action="store_true",
                    help="show what would happen without moving files")
    args = ap.parse_args()

    INBOX.mkdir(exist_ok=True)
    OUTBOX.mkdir(exist_ok=True)

    photos = sorted(
        [p for p in INBOX.iterdir() if p.suffix.lower() in IMAGE_EXTS],
        key=capture_time,
    )
    if not photos:
        print(f"No images found in {INBOX.resolve()}. Drop photos there and rerun.")
        sys.exit(0)

    n = args.shots
    roles = ROLE_NAMES[n]
    if len(photos) % n != 0:
        print(f"⚠ {len(photos)} photos is not a multiple of {n}.")
        print("  The last incomplete group will be skipped — check for a missed shot.")

    groups = [photos[i:i + n] for i in range(0, len(photos) - len(photos) % n, n)]
    print(f"Found {len(photos)} photos → {len(groups)} coins ({n} shots each)\n")

    sb = supabase_client()
    current_id = args.start or next_id_from_csv(CSV_LOG)

    for gi, group in enumerate(groups, 1):
        first = group[0]
        t = datetime.fromtimestamp(capture_time(first)).strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{gi}/{len(groups)}] {' + '.join(p.name for p in group)}  (shot {t})")

        if args.auto:
            coin_id = current_id
        else:
            entered = input(f"  coin_id [{current_id}]: ").strip().upper()
            coin_id = entered or current_id
            if entered.lower() in {"s", "skip"}:
                print("  skipped\n")
                continue

        row = {f: "" for f in CSV_FIELDS}
        row["coin_id"] = coin_id
        row["shot_time"] = t
        row["status"] = "photographed"
        row["created_at"] = datetime.now().isoformat(timespec="seconds")

        for photo, role in zip(group, roles):
            new_name = f"{coin_id}-{role}{photo.suffix.lower()}"
            dest = OUTBOX / new_name
            if dest.exists():
                print(f"  ⚠ {new_name} already exists in outbox — skipping this coin entirely.")
                break
            if args.dry_run:
                print(f"  would rename {photo.name} → {new_name}")
            else:
                shutil.move(str(photo), dest)
                print(f"  {photo.name} → {new_name}")
            row[f"photo_{role}"] = new_name
        else:
            if not args.dry_run:
                append_csv(row)
                push_supabase(sb, row)
            current_id = bump_id(coin_id) if coin_id == current_id else next_id_from_csv(CSV_LOG)
            print()
            continue
        print()  # group was aborted due to collision

    print("Done." + (" (dry run — nothing moved)" if args.dry_run else f" Log: {CSV_LOG.resolve()}"))


if __name__ == "__main__":
    main()
