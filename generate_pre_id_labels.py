#!/usr/bin/env python3
"""
generate_pre_id_labels.py — print a batch of pre-ID labels for the
CL-<date>-BOX<box>-PS<photoset>-<item> coin labeling system.

Uses today's date automatically. Auto-detects the next unused item number
for a given box/photo-set by scanning any previously generated
pre_id_labels_*.md files in this directory, so you don't have to track the
last number by hand.

Usage:
  python3 generate_pre_id_labels.py --count 500
  python3 generate_pre_id_labels.py --box 2 --photoset 1 --count 200
  python3 generate_pre_id_labels.py --box 1 --photoset 1 --start 502 --count 100
  python3 generate_pre_id_labels.py --date 20260710 --count 50 --out custom.md
  python3 generate_pre_id_labels.py --count 500 --qr   # also generate a QR code per label
  python3 generate_pre_id_labels.py --count 100 --thermal   # + one ready-to-print PNG per label

Run with the project .venv if using --qr/--thermal (needs qrcode + Pillow):
  .venv/bin/python3 generate_pre_id_labels.py --count 500 --qr
  .venv/bin/python3 generate_pre_id_labels.py --count 100 --thermal

--thermal is for mini Bluetooth thermal label printers (e.g. via the
Walkprint app): one PNG per label, QR code stacked over the text, sized to
the printer's paper width (default 384px = 58mm at 203dpi - pass --width to
match your printer/paper). Import that folder's images into the app and
print each one; no markdown/checklist needed for this path.
"""
import argparse
import glob
import os
import re
from datetime import datetime

LABEL_RE = re.compile(r"CL-(\d{8})-BOX(\d+)-PS(\d+)-(\d+)")
QR_DIR = "qr_codes"
THERMAL_DIR = "thermal_labels"


def find_next_start(date, box, photoset):
    """Scan existing pre_id_labels_*.md files for the highest item number
    already generated under this exact date/box/photoset, return the next one."""
    highest = 0
    for path in glob.glob("pre_id_labels_*.md"):
        with open(path) as f:
            text = f.read()
        for m in LABEL_RE.finditer(text):
            d, b, ps, item = m.groups()
            if d == date and int(b) == box and int(ps) == photoset:
                highest = max(highest, int(item))
    return highest + 1


def make_qr(label, out_dir):
    import qrcode
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{label}.png")
    img = qrcode.make(label, box_size=4, border=1)
    img.save(path)
    return path


def make_thermal_label(label, out_dir, width):
    """One ready-to-print PNG: QR code on top, label text below, sized to
    the thermal printer's paper width. Splits the label onto two lines
    (CL-date-BOXnn / PSnnn-item) so it stays legible on narrow paper."""
    import qrcode
    from PIL import Image, ImageDraw, ImageFont

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{label}.png")

    m = LABEL_RE.match(label)
    date, box, photoset, item = m.groups()
    line1 = f"CL-{date}-BOX{box}"
    line2 = f"PS{photoset}-{item}"

    qr_size = int(width * 0.6)
    qr_img = qrcode.make(label, box_size=10, border=1).resize((qr_size, qr_size))

    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(width * 0.09))
    except Exception:
        font = ImageFont.load_default()

    pad = int(width * 0.04)
    text_h = int(width * 0.09 * 2.6)  # two lines + spacing
    height = pad + qr_size + pad + text_h + pad

    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    img.paste(qr_img, ((width - qr_size) // 2, pad))

    y = pad + qr_size + pad
    for line in (line1, line2):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(((width - tw) // 2, y), line, fill=0, font=font)
        y += bbox[3] - bbox[1] + int(width * 0.03)

    img.save(path)
    return path


def main():
    ap = argparse.ArgumentParser(description="Generate a batch of pre-ID coin labels.")
    ap.add_argument("--box", type=int, default=1, help="box number (default 1)")
    ap.add_argument("--photoset", type=int, default=1, help="photo set number (default 1)")
    ap.add_argument("--count", type=int, required=True, help="how many labels to generate")
    ap.add_argument("--start", type=int, default=None,
                    help="starting item number (default: auto-detect next unused for this date/box/photoset)")
    ap.add_argument("--date", type=str, default=None,
                    help="override date as YYYYMMDD (default: today)")
    ap.add_argument("--out", type=str, default=None,
                    help="output markdown file (default: pre_id_labels_<date>_BOX<box>_PS<photoset>.md)")
    ap.add_argument("--qr", action="store_true",
                    help="also generate a scannable QR code per label, embedded next to the text in the markdown")
    ap.add_argument("--thermal", action="store_true",
                    help="generate one ready-to-print PNG per label (QR + text) for a mini Bluetooth thermal printer/app")
    ap.add_argument("--width", type=int, default=384,
                    help="thermal label width in px (default 384 = 58mm at 203dpi)")
    args = ap.parse_args()

    date = args.date or datetime.now().strftime("%Y%m%d")
    start = args.start if args.start is not None else find_next_start(date, args.box, args.photoset)
    out_path = args.out or f"pre_id_labels_{date}_BOX{args.box:02d}_PS{args.photoset:03d}.md"

    labels = [
        f"CL-{date}-BOX{args.box:02d}-PS{args.photoset:03d}-{i:04d}"
        for i in range(start, start + args.count)
    ]

    lines = [
        f"# Pre-ID Label Batch — CL-{date}-BOX{args.box:02d}-PS{args.photoset:03d}",
        "",
        f"{args.count} pre-ID labels, item numbers {start:04d}-{start + args.count - 1:04d}.",
        "Format: `CL-<date>-BOX<box>-PS<photo set>-<item>`. Check each off as you",
        "print and attach it to a coin, before identification.",
        "",
    ]

    if args.qr:
        qr_subdir = os.path.join(QR_DIR, f"{date}_BOX{args.box:02d}_PS{args.photoset:03d}")
        for label in labels:
            qr_path = make_qr(label, qr_subdir)
            lines.append(f"- [ ] ![]({qr_path}) `{label}`")
    else:
        lines += [f"- [ ] {label}" for label in labels]

    with open(out_path, "w") as f:
        f.write("\n".join(lines) + "\n")

    qr_note = f" + QR codes in {QR_DIR}/{date}_BOX{args.box:02d}_PS{args.photoset:03d}/" if args.qr else ""
    print(f"Wrote {args.count} labels ({start:04d}-{start + args.count - 1:04d}) to {out_path}{qr_note}")

    if args.thermal:
        thermal_subdir = os.path.join(THERMAL_DIR, f"{date}_BOX{args.box:02d}_PS{args.photoset:03d}")
        for label in labels:
            make_thermal_label(label, thermal_subdir, args.width)
        print(f"Wrote {args.count} thermal-print PNGs ({args.width}px wide) to {thermal_subdir}/")


if __name__ == "__main__":
    main()
