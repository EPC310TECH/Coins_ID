"""
batch_report.py - one command for a box of coins:

    detect (Roboflow) -> crop -> read date (Claude Opus 4.8) -> flag key dates
    -> write BATCH_<date>.md  (+ raw JSON)

The date reader also names the series, so it doubles as the identifier here - it
outperforms the CLIP matcher on a clean full-res crop and is the same read the
key-date flags need. Shoot coins front+back: US coins carry the date only on the
obverse, so each coin yields one dated (obverse) row; reverses come back
date-less and are counted, not listed.

Usage:
    python batch_report.py <image-or-dir> [more ...] [--date YYYYMMDD]
                           [--box N] [--photoset N] [--out FILE]

Needs ROBOFLOW_* and ANTHROPIC_API_KEY in .env (gitignored). Costs ~$0.01/coin
(Batch API). Reuses coin_detect's detector/cropper and read_coin_date's reader.
"""
import argparse
import collections
import glob
import json
import os
from datetime import datetime

from PIL import Image, ImageOps

from coin_detect import (load_env, detect_workflow, detect_roboflow,
                         crop_detection, DEFAULT_API_URL)
from read_coin_date import read_batch
from rare_flags import flag

CROP_DIR = "batch_report_crops"
IMG_EXTS = (".jpg", ".jpeg", ".png")
RED = "\U0001F534"


def _detect(image_path, env):
    """Use whichever Roboflow backend is configured (workflow preferred)."""
    if env.get("ROBOFLOW_WORKFLOW_ID"):
        return detect_workflow(
            image_path, env.get("ROBOFLOW_WORKSPACE"), env["ROBOFLOW_WORKFLOW_ID"],
            env.get("ROBOFLOW_CLASSES", "coin"), env["ROBOFLOW_API_KEY"],
            env.get("ROBOFLOW_API_URL", DEFAULT_API_URL),
        )
    return detect_roboflow(image_path, env["ROBOFLOW_MODEL"], env["ROBOFLOW_API_KEY"],
                           env.get("ROBOFLOW_API_URL", DEFAULT_API_URL))


def _expand(inputs):
    paths = []
    for item in inputs:
        if os.path.isdir(item):
            paths += [p for p in sorted(glob.glob(os.path.join(item, "*")))
                      if p.lower().endswith(IMG_EXTS)]
        elif item.lower().endswith(IMG_EXTS):
            paths.append(item)
    return paths


def _flag_for(r):
    mm = r.get("mint_mark")
    known = mm not in (None, "none", "unknown")
    return flag({
        "year": r.get("year"),
        "mint_mark": "P" if mm == "none" else (mm if known else "not legible in photo"),
        "design_variety": r.get("series", ""),
        "denomination": r.get("denomination", ""),
        "category": f"Circulating {str(r.get('denomination', '')).title()}",
        "wheat_reverse": "wheat" in str(r.get("series", "")).lower(),
    })


def _denom(r):
    text = (str(r.get("denomination", "")) + " " + str(r.get("series", ""))).lower()
    for k in ("quarter", "dime", "nickel", "half dollar", "dollar", "cent"):
        if k in text:
            return k
    return "?"


def build(images, date, box, photoset, out_path):
    env = load_env()
    os.makedirs(CROP_DIR, exist_ok=True)

    crop_paths = []
    for image_path in images:
        dets = _detect(image_path, env)
        img = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")
        stem = os.path.splitext(os.path.basename(image_path))[0]
        for i, det in enumerate(sorted(dets, key=lambda d: (d["y0"], d["x0"]))):
            out = os.path.join(CROP_DIR, f"{stem}_det{i:02d}.jpg")
            crop_detection(img, det, out)
            crop_paths.append(out)
    print(f"detected + cropped {len(crop_paths)} coins across {len(images)} images")

    reads = read_batch(crop_paths)
    raw = {os.path.basename(p): r for p, r in zip(crop_paths, reads)}
    json_path = out_path.rsplit(".", 1)[0] + ".json"
    with open(json_path, "w") as f:
        json.dump(raw, f, indent=0)

    coins, reverses, unreadable, flags = [], 0, 0, []
    for r in reads:
        if not isinstance(r, dict) or r.get("error"):
            unreadable += 1
            continue
        if r.get("year"):
            coins.append(r)
            hit, why = _flag_for(r)
            if hit:
                flags.append((r, why))
        elif r.get("side") == "reverse":
            reverses += 1
        else:
            unreadable += 1

    den = collections.Counter(_denom(r) for r in coins)
    L = [f"# Batch results - {date} (BOX{box:02d} / PS{photoset:03d})", ""]
    L.append(f"{len(coins)} coins dated, run through detect -> crop -> identify -> "
             f"date-read -> flag. ({len(coins)} obverses, {reverses} reverses, "
             f"{unreadable} unreadable/partial.)")
    L += ["", "**Composition:** " + ", ".join(f"{n} {k}" for k, n in den.most_common()) + ".", ""]

    L += ["## Flagged for a closer look", ""]
    if flags:
        for r, why in flags:
            mm = r.get("mint_mark")
            d = f"{r['year']}-{mm}" if mm not in (None, "none", "unknown") else str(r["year"])
            L.append(f"- **{d} {r.get('series', '')}** {RED} - {why}")
    else:
        L.append("_None - no key dates or silver in this batch._")

    L += ["", "## All dated coins", "", "| Date | Series | Denom | Conf | Flag |", "|---|---|---|---|---|"]
    for r in sorted(coins, key=lambda x: (x.get("year") or 0)):
        mm = r.get("mint_mark")
        d = f"{r['year']}-{mm}" if mm not in (None, "none", "unknown") else str(r["year"])
        fl = RED if _flag_for(r)[0] else ""
        L.append(f"| {d} | {str(r.get('series',''))[:42]} | {_denom(r)} | {r.get('confidence','')} | {fl} |")

    with open(out_path, "w") as f:
        f.write("\n".join(L) + "\n")
    print(f"\nwrote {out_path}  ({len(coins)} coins, {len(flags)} flagged)")
    print(f"raw reads -> {json_path}")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="Detect -> identify -> date -> flag -> BATCH_<date>.md")
    ap.add_argument("inputs", nargs="+", help="image files and/or directories")
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--box", type=int, default=1)
    ap.add_argument("--photoset", type=int, default=1)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    images = _expand(args.inputs)
    if not images:
        raise SystemExit("no images found in the given paths")
    out = args.out or f"BATCH_{args.date}.md"
    build(images, args.date, args.box, args.photoset, out)


if __name__ == "__main__":
    main()
