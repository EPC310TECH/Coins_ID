import sys

import numpy as np
import open_clip
import torch
from PIL import Image

from build_embeddings import MODEL_NAME, PRETRAINED, device

EMBEDDINGS_PATH = "training_embeddings.npz"


def load_index():
    data = np.load(EMBEDDINGS_PATH, allow_pickle=True)
    return data


_model = None
_preprocess = None


def _get_model():
    global _model, _preprocess
    if _model is None:
        dev = device()
        _model, _, _preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED)
        _model = _model.to(dev).eval()
    return _model, _preprocess


def embed_image(path):
    model, preprocess = _get_model()
    dev = device()
    img = Image.open(path).convert("RGB")
    tensor = preprocess(img).unsqueeze(0).to(dev)
    with torch.no_grad():
        feat = model.encode_image(tensor)
        feat = feat / feat.norm(dim=-1, keepdim=True)
    return feat.cpu().numpy()[0]


def identify(path, top_k=5):
    data = load_index()
    query = embed_image(path)
    sims = data["embeddings"] @ query  # cosine similarity (already L2-normalized)
    order = np.argsort(-sims)[:top_k]
    results = []
    for idx in order:
        results.append({
            "file": str(data["files"][idx]),
            "class_label": str(data["class_labels"][idx]),
            "denomination": str(data["denominations"][idx]),
            "year": str(data["years"][idx]),
            "source_type": str(data["source_types"][idx]),
            "label_confidence": str(data["confidences"][idx]),
            "similarity": float(sims[idx]),
        })
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 identify_coin.py <image_path> [top_k]")
        sys.exit(1)
    path = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    for r in identify(path, top_k):
        print(f"{r['similarity']:.3f}  {r['class_label']:<55} {r['year']:<12} ({r['file']}, label conf: {r['label_confidence']})")
