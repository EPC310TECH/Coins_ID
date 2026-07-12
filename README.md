# Coins_ID

A computer-vision pipeline for identifying, flagging, and inventorying U.S. coins
from photos — built around a CLIP reference-gallery matcher rather than a trained
classifier, so new coin types can be added by dropping in labeled reference images
and rebuilding the embedding index.

## Pipeline

```
photo ──▶ detect + crop ──▶ identify ──▶ flag ──▶ inventory / labels
          (coin_detect.py)  (identify_   (rare_    (build_inventory.py,
                             coin.py)     flags.py)  generate_report.py,
                                                     generate_pre_id_labels.py)
```

1. **Detect + crop** (`coin_detect.py`) — locate every coin in a batch/pile photo
   and crop each one. Two Roboflow backends (see [Auto-crop](#auto-crop)); falls
   back to hand-laid boxes in `coin_boxes.py` for archived photos.
2. **Identify** (`identify_coin.py`) — embed each crop with CLIP (`ViT-B-32`,
   OpenAI weights) and match against a labeled reference gallery by cosine
   similarity. Supports an optional **denomination prior**.
3. **Flag** (`rare_flags.py`) — surface key-date / variety candidates (wheat
   cents, pre-1965 silver, war nickels, etc.) for a closer look.
4. **Inventory & labels** (`build_inventory.py`, `generate_report.py`,
   `generate_pre_id_labels.py`) — physical specs from `coin_specs.py`, a CSV
   inventory, an HTML report, and thermal-printer labels; optional Supabase sync.

## Results

**Held-out accuracy** — measured with `eval_wikimedia_heldout.py` on 120
Wikimedia Commons photos (12 images × 10 coin types) that are **not** in the
reference gallery:

| Setting | Top-1 accuracy |
|---|---|
| Baseline (nearest-neighbor) | **45%** |
| + denomination prior (detector-realistic) | **57%** |
| + denomination prior (oracle ceiling) | 68% |

- Strong on well-referenced common coins (~70%: Lincoln cent, Jefferson nickel,
  Washington quarter), weaker on sparse half-dollars/dollars/dimes — a reference
  *coverage* gap, not a code issue.
- The **denomination prior** constrains the match to the detector's denomination
  (Penny/Nickel/Dime/Quarter). It lifts top-1 by ~12 points; e.g. Roosevelt dime
  goes from 2/12 → 10/12 because dimes stop collapsing onto the dense quarter
  references.
- Removing 540 side-less "unknown side" quarter references (generic "silver disc"
  attractors) lifted the baseline from 42% → 45% with no class regressing.

**Reference gallery:** 4,635 labeled CLIP embeddings (`training_embeddings.npz`)
drawn from the user's own collection crops, a historic type-set reference set,
modern bullion/proof issues, the Hugging Face `UsCoinsCommon` set
(Lincoln/Jefferson/Washington), and the Kaggle rare-US-coin set
(Eisenhower / Franklin / Kennedy / Susan B. Anthony).

## Auto-crop

`coin_detect.py` localizes coins via a Roboflow-hosted backend, then feeds crops
to `identify_coin.py`. Two backends, selected by `.env` config:

| Backend | Output | Trade-off |
|---|---|---|
| Segmentation workflow (`general-segmentation-api-2`) | generic `coin` masks + boxes | cleanest counts, no denomination prior |
| Detection model (`us-coins-qjnn6/1`) | Penny/Nickel/Dime/Quarter | enables the +12-point denomination prior |

The workflow backend takes precedence when configured. Detector crops are written
to `detected_crops/` (gitignored), separate from the curated `coin_crops/`.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install torch open_clip_torch huggingface_hub pillow numpy inference-sdk
```

Secrets and model IDs live in a gitignored `.env` (never in code):

```
ROBOFLOW_API_KEY=...
ROBOFLOW_API_URL=https://serverless.roboflow.com
# Backend A — segmentation workflow (preferred when set):
ROBOFLOW_WORKSPACE=antonio-jasso
ROBOFLOW_WORKFLOW_ID=general-segmentation-api-2
ROBOFLOW_CLASSES=coin
# Backend B — detection model (denomination prior):
ROBOFLOW_MODEL=us-coins-qjnn6/1
```

## Usage

```bash
# Build / rebuild the reference embedding index
python build_embeddings.py

# Identify a single cropped coin (ranked matches)
python identify_coin.py path/to/coin.jpg 5

# Auto-detect + crop + identify every coin in a batch photo
python coin_detect.py path/to/batch.jpg
python coin_detect.py path/to/batch.jpg --no-prior          # ignore detector denomination
python coin_detect.py path/to/batch.jpg --detections d.json # offline, hand-supplied boxes

# Re-run the held-out accuracy benchmark
python eval_wikimedia_heldout.py 12
```

## Repository layout

| File | Purpose |
|---|---|
| `identify_coin.py` | CLIP nearest-neighbor matcher + denomination prior |
| `coin_detect.py` | Roboflow detect/segment → crop → identify |
| `build_embeddings.py` | Build `training_embeddings.npz` from the manifests |
| `build_training_manifest.py` | User crops + type-set + bullion references |
| `build_hf_common_coins_manifest.py` | Hugging Face common-coin bridge (local-only) |
| `build_rare_us_coins_manifest.py` | Kaggle rare-US-coin bridge (local-only) |
| `eval_wikimedia_heldout.py` | Held-out accuracy benchmark |
| `rare_flags.py` | Key-date / variety flagging rules |
| `coin_specs.py` | U.S. Mint physical specifications |
| `coin_boxes.py` / `crop.py` | Legacy hand-laid crop boxes |
| `build_inventory.py` / `generate_report.py` | Inventory CSV + HTML report |
| `generate_pre_id_labels.py` | Thermal-printer coin labels |
| `coin_intake.py` / `schema.sql` | Intake + optional Supabase sync |

## Notes

- Raw reference images and machine-specific manifests stay local (gitignored);
  only the resulting `training_embeddings.npz` is committed.
- Accuracy is bounded by reference-image *variety* for the sparse classes — a
  pure-vision matcher has no size/weight signal, so real-world toned/slabbed
  half-dollars and dollars remain the hardest cases.
