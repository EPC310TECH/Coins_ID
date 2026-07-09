import csv

import numpy as np
import open_clip
import torch
from PIL import Image

MANIFEST_PATH = "training_manifest.csv"
OUT_PATH = "training_embeddings.npz"
MODEL_NAME = "ViT-B-32-quickgelu"
PRETRAINED = "openai"


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

    np.savez(
        OUT_PATH,
        embeddings=embeddings, files=files, class_labels=class_labels,
        denominations=denominations, years=years, source_types=source_types,
        confidences=confidences, model_name=MODEL_NAME, pretrained=PRETRAINED,
    )
    print(f"Wrote {len(kept_rows)} embeddings ({embeddings.shape[1]}-dim) to {OUT_PATH}")


if __name__ == "__main__":
    build()
