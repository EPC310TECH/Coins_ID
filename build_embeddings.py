import csv
import os
import re

import numpy as np
import open_clip
import torch
from PIL import Image

MANIFEST_PATH = "training_manifest.csv"
LOCAL_ONLY_MANIFESTS = ["hf_common_coins_manifest.csv", "rare_us_coins_manifest.csv"]
OUT_PATH = "training_embeddings.npz"
MODEL_NAME = "ViT-B-32-quickgelu"
PRETRAINED = "openai"

# CLIP is a joint image-TEXT model, so each class also gets a text "anchor":
# the class name encoded by the text tower. Sparse classes (halves, dollars)
# have too few reference images to win a nearest-neighbour vote against the
# thousands of Lincoln cents, but their *name* is unambiguous to CLIP. See
# identify_coin.identify(text_fusion=True), which fuses the two scores.
TEXT_TEMPLATES = [
    "a photo of a {}",
    "a close-up photo of a {} coin",
    "a {} coin",
    "the obverse of a {} coin",
    "the reverse of a {} coin",
    "a worn {} coin",
]


def clean_label(label):
    """Side markers and long free-text descriptions make poor prompts."""
    label = re.sub(r"\s*\((obverse|reverse|unknown side)\)\s*", " ", label, flags=re.I)
    label = re.sub(r"\s+", " ", label).strip()
    return label[:150]


def build_text_anchors(model, labels, dev):
    tokenizer = open_clip.get_tokenizer(MODEL_NAME)
    anchors = []
    with torch.no_grad():
        for label in labels:
            prompts = [t.format(clean_label(label)) for t in TEXT_TEMPLATES]
            feats = model.encode_text(tokenizer(prompts).to(dev))
            feats = feats / feats.norm(dim=-1, keepdim=True)
            mean = feats.mean(0)
            anchors.append((mean / mean.norm()).cpu().numpy())
    return np.stack(anchors).astype(np.float32)


def device():
    if torch.backends.mps.is_available():
        return "mps"
    return "cuda" if torch.cuda.is_available() else "cpu"


def build():
    dev = device()
    print(f"Loading {MODEL_NAME} ({PRETRAINED}) on {dev}...")
    model, _, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
    model = model.to(dev).eval()

    with open(MANIFEST_PATH, newline="") as f:
        rows = list(csv.DictReader(f))
    for path in LOCAL_ONLY_MANIFESTS:
        if os.path.exists(path):
            with open(path, newline="") as f:
                extra = list(csv.DictReader(f))
            print(f"  + {len(extra)} rows from local-only {path}")
            rows.extend(extra)

    embeddings = []
    kept_rows = []
    with torch.no_grad():
        for i, row in enumerate(rows):
            path = row["file"]
            try:
                img = Image.open(path).convert("RGB")
            except Exception as e:
                print(f"  skip {row['file']}: {e}")
                continue
            tensor = preprocess(img).unsqueeze(0).to(dev)
            feat = model.encode_image(tensor)
            feat = feat / feat.norm(dim=-1, keepdim=True)
            embeddings.append(feat.cpu().numpy()[0])
            kept_rows.append(row)
            if (i + 1) % 50 == 0:
                print(f"  {i + 1}/{len(rows)}")

    embeddings = np.stack(embeddings).astype(np.float32)
    files = np.array([r["file"] for r in kept_rows])
    class_labels = np.array([r["class_label"] for r in kept_rows])
    denominations = np.array([r["denomination"] for r in kept_rows])
    years = np.array([r["year"] for r in kept_rows])
    source_types = np.array([r["source_type"] for r in kept_rows])
    confidences = np.array([r["confidence"] for r in kept_rows])

    anchor_labels = sorted(set(class_labels.tolist()))
    print(f"Encoding text anchors for {len(anchor_labels)} distinct classes...")
    anchor_embeddings = build_text_anchors(model, anchor_labels, dev)

    np.savez(
        OUT_PATH,
        embeddings=embeddings, files=files, class_labels=class_labels,
        denominations=denominations, years=years, source_types=source_types,
        confidences=confidences, model_name=MODEL_NAME, pretrained=PRETRAINED,
        anchor_labels=np.array(anchor_labels), anchor_embeddings=anchor_embeddings,
    )
    print(f"Wrote {len(kept_rows)} embeddings ({embeddings.shape[1]}-dim) "
          f"+ {len(anchor_labels)} text anchors to {OUT_PATH}")


if __name__ == "__main__":
    build()
