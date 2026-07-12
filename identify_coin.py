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


def canon_denomination(s):
    """Collapse a free-text denomination (from the gallery or a detector) to a
    canonical token, or None if it's ambiguous/unknown. Order matters:
    'half dollar' before 'dollar', 'nickel' before 'cent' ("Nickel (5 cents)")."""
    t = str(s).lower()
    if "uncertain" in t:
        return None
    if "half" in t and "dollar" in t:  # "half dollar", "half-dollar", "half_dollar"
        return "half_dollar"
    if "dollar" in t:
        return "dollar"
    if "quarter" in t and "eagle" not in t:  # exclude "$2.50 Quarter Eagle" gold
        return "quarter"
    if "dime" in t:
        return "dime"
    if "nickel" in t:
        return "nickel"
    if "cent" in t or "penny" in t:
        return "cent"
    return None


def identify(path, top_k=5, denomination=None):
    """Nearest-neighbour identify. If `denomination` is given (e.g. a detector's
    coarse call like 'quarter'), the search is restricted to gallery entries of
    that denomination plus ambiguous ones - a soft prior, not a hard gate."""
    data = load_index()
    query = embed_image(path)
    sims = data["embeddings"] @ query  # cosine similarity (already L2-normalized)
    candidates = np.arange(len(sims))
    target = canon_denomination(denomination) if denomination else None
    if target:
        keep = np.array([
            canon_denomination(dn) in (target, None) for dn in data["denominations"]
        ])
        if keep.any():
            candidates = candidates[keep]
    order = candidates[np.argsort(-sims[candidates])[:top_k]]
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
