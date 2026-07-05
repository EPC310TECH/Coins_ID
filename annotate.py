import os

from PIL import Image, ImageDraw, ImageFont

from coin_boxes import COIN_BOXES

IMAGES_DIR = "coin_images"
CROPS_DIR = "coin_crops"
ANNOTATED_DIR = "annotated"

FLAG_COLOR = (230, 30, 30)
NORMAL_COLOR = (40, 160, 60)


def _font(size=28):
    try:
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except Exception:
        return ImageFont.load_default()


def build_all():
    os.makedirs(CROPS_DIR, exist_ok=True)
    os.makedirs(ANNOTATED_DIR, exist_ok=True)
    font = _font()

    for image_name, boxes in COIN_BOXES.items():
        src_path = os.path.join(IMAGES_DIR, image_name)
        if not os.path.exists(src_path):
            print(f"missing source image: {src_path}")
            continue
        img = Image.open(src_path).convert("RGB")
        w, h = img.size
        annotated = img.copy()
        draw = ImageDraw.Draw(annotated)

        for box in boxes:
            x0, y0, x1, y1 = box["x0"] * w, box["y0"] * h, box["x1"] * w, box["y1"] * h
            color = FLAG_COLOR if box.get("flagged") else NORMAL_COLOR

            # crop this coin out to its own file
            pad = 0.01
            cx0 = max(0, int((box["x0"] - pad) * w))
            cy0 = max(0, int((box["y0"] - pad) * h))
            cx1 = min(w, int((box["x1"] + pad) * w))
            cy1 = min(h, int((box["y1"] + pad) * h))
            crop = img.crop((cx0, cy0, cx1, cy1))
            crop_name = f"{os.path.splitext(image_name)[0]}_{box['id']}.jpg"
            crop.save(os.path.join(CROPS_DIR, crop_name), quality=90)
            box["_crop_file"] = crop_name

            # draw the box + label on the annotated overlay
            draw.rectangle([x0, y0, x1, y1], outline=color, width=5)
            label = box["id"] + (" ★" if box.get("flagged") else "")
            tb = draw.textbbox((0, 0), label, font=font)
            tw, th = tb[2] - tb[0], tb[3] - tb[1]
            draw.rectangle([x0, y0 - th - 8, x0 + tw + 8, y0], fill=color)
            draw.text((x0 + 4, y0 - th - 6), label, fill=(255, 255, 255), font=font)

        annotated.save(os.path.join(ANNOTATED_DIR, image_name), quality=88)
        print(f"{image_name}: {len(boxes)} boxes -> annotated/{image_name}")


if __name__ == "__main__":
    build_all()
