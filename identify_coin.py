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


# Image weight in text fusion; (1 - alpha) goes to the text anchor. Tuned on the
# 120-image Wikimedia held-out set with anchors for all 170 gallery classes:
# 1.0 (no fusion) = 45%, 0.8 = 51%, 0.5 = 50%, 0.4 = 48%, 0.0 (pure text) = 36%.
# A closed-set prototype over only 10 clean class names preferred 0.4, but with
# 170 classes - many carrying long free-text labels - the anchors are noisier, so
# text gets a smaller share.
DEFAULT_ALPHA = 0.8


def _result(data, idx, similarity):
    return {
        "file": str(data["files"][idx]),
        "class_label": str(data["class_labels"][idx]),
        "denomination": str(data["denominations"][idx]),
        "year": str(data["years"][idx]),
        "source_type": str(data["source_types"][idx]),
        "label_confidence": str(data["confidences"][idx]),
        "similarity": float(similarity),
    }


def _minmax(v):
    span = v.max() - v.min()
    return (v - v.min()) / span if span else np.zeros_like(v)


def identify(path, top_k=5, denomination=None, text_fusion=False, alpha=DEFAULT_ALPHA):
    """Identify a cropped coin against the reference gallery.

    denomination: soft prior (e.g. a detector's 'quarter') - restricts the search
        to that denomination plus ambiguous entries.
    text_fusion: score each *class* by fusing its best image match with its CLIP
        text anchor. Raw nearest-neighbour lets dense classes (thousands of
        Lincoln cents) swamp sparse ones (halves, dollars); the text anchor is
        independent of how many reference images a class happens to have, so it
        rescues them. Can't be done by simply adding anchors to the gallery -
        the modality gap (image-text sim ~0.25 vs image-image ~0.85) means a
        text anchor would never win a raw nearest-neighbour vote.
    """
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

    if not text_fusion or "anchor_labels" not in data.files:
        order = candidates[np.argsort(-sims[candidates])[:top_k]]
        return [_result(data, i, sims[i]) for i in order]

    # --- class-level fused scoring ---
    labels = data["class_labels"]
    text_sims = data["anchor_embeddings"] @ query
    anchor_of = {str(l): float(s) for l, s in zip(data["anchor_labels"], text_sims)}

    best = {}  # class_label -> (entry index, image similarity)
    for i in candidates:
        label = str(labels[i])
        if label not in best or sims[i] > best[label][1]:
            best[label] = (i, float(sims[i]))

    classes = list(best)
    img = np.array([best[c][1] for c in classes])
    txt = np.array([anchor_of.get(c, float(text_sims.min())) for c in classes])
    fused = alpha * _minmax(img) + (1 - alpha) * _minmax(txt)

    results = []
    for j in np.argsort(-fused)[:top_k]:
        idx, sim = best[classes[j]]
        row = _result(data, idx, sim)
        row["fused_score"] = float(fused[j])
        results.append(row)
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python3 identify_coin.py <image_path> [top_k]")
        sys.exit(1)
    path = sys.argv[1]
    top_k = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    for r in identify(path, top_k):
        print(f"{r['similarity']:.3f}  {r['class_label']:<55} {r['year']:<12} ({r['file']}, label conf: {r['label_confidence']})")
