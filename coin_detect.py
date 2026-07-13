"""
Automatic coin localization: find every coin in a batch/pile photo, crop each
one, and hand the crops to the CLIP identifier - replacing the hand-laid
fractional boxes in coin_boxes.py.

Localization uses a Roboflow-hosted object detector (default model
us-coins-qjnn6/1, classes Penny/Nickel/Dime/Quarter) via the inference-sdk
serverless API. The detector's coarse denomination is passed to identify() as a
*soft prior* (identify_coin.canon_denomination) to sharpen the fine-series
match. Caveat: the detector has no half-dollar or dollar class, so for those
coins its denomination is unreliable - use --no-prior (or trust the CLIP series
match over the detector's denomination) on batches that contain halves/dollars.

Two localizer backends are supported (config in .env, which is gitignored):
    ROBOFLOW_API_KEY=...              (required)
    ROBOFLOW_API_URL=https://serverless.roboflow.com   (optional, this default)
  A) Segmentation workflow (preferred when set) - generic "coin" localization,
     no denomination prior, cleaner counts + polygon masks:
    ROBOFLOW_WORKFLOW_ID=general-segmentation-api-2
    ROBOFLOW_WORKSPACE=antonio-jasso
    ROBOFLOW_CLASSES=coin
  B) Object-detection model - gives a denomination for the soft prior:
    ROBOFLOW_MODEL=us-coins-qjnn6/1
Usage:
    python coin_detect.py <image> [out_dir]            # detect + crop + identify
    python coin_detect.py <image> --detections d.json  # offline: skip the API,
                                                        # use hand/synthetic boxes
    python coin_detect.py <image> --no-prior           # ignore detector denom
"""
import json
import os
import sys

from PIL import Image, ImageOps

from identify_coin import identify, canon_denomination

DEFAULT_API_URL = "https://serverless.roboflow.com"
CROP_DIR_DEFAULT = "detected_crops"  # kept separate from the curated coin_crops/
PAD = 0.08          # fraction of box size added on each side so the rim isn't clipped
MIN_CONFIDENCE = 0.40


def load_env(path=".env"):
    env = {}
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    # real environment overrides .env
    env.update({k: v for k, v in os.environ.items() if k.startswith("ROBOFLOW_")})
    return env


def detect_roboflow(image_path, model, api_key, api_url=DEFAULT_API_URL, min_conf=MIN_CONFIDENCE):
    """Run the Roboflow-hosted detector via inference-sdk; return normalized,
    confidence-filtered detections."""
    from inference_sdk import InferenceHTTPClient
    client = InferenceHTTPClient(api_url=api_url, api_key=api_key)
    payload = client.infer(image_path, model_id=model)
    return [d for d in _normalize(payload) if d["confidence"] >= min_conf]


def detect_workflow(image_path, workspace, workflow_id, classes, api_key,
                    api_url=DEFAULT_API_URL, min_conf=MIN_CONFIDENCE):
    """Run a promptable-segmentation Roboflow *workflow* (class prompts in
    `classes`, e.g. 'coin') and return normalized, confidence-filtered
    detections. Generic 'coin' class => no denomination prior, but cleaner
    localization; polygon masks (points) are preserved for optional tight crops."""
    from inference_sdk import InferenceHTTPClient
    client = InferenceHTTPClient(api_url=api_url, api_key=api_key)
    result = client.run_workflow(
        workspace_name=workspace, workflow_id=workflow_id,
        images={"image": image_path},
        parameters={"classes": classes}, use_cache=True,
    )
    block = (result[0] if isinstance(result, list) else result)["predictions"]
    dets = _normalize(block)
    for det, p in zip(dets, block.get("predictions", [])):
        if p.get("points"):
            det["points"] = p["points"]
    return [d for d in dets if d["confidence"] >= min_conf]


def _normalize(payload):
    """Roboflow returns center x/y + width/height in pixels; convert to
    fractional x0/y0/x1/y1 boxes and a canonical denomination."""
    W = payload.get("image", {}).get("width")
    H = payload.get("image", {}).get("height")
    dets = []
    for p in payload.get("predictions", []):
        cx, cy, w, h = p["x"], p["y"], p["width"], p["height"]
        dets.append({
            "x0": (cx - w / 2) / W, "y0": (cy - h / 2) / H,
            "x1": (cx + w / 2) / W, "y1": (cy + h / 2) / H,
            "raw_class": p.get("class", ""),
            "denomination": canon_denomination(p.get("class", "")),
            "confidence": float(p.get("confidence", 0.0)),
        })
    return dets


def crop_detection(img, det, out_path, pad=PAD, upscale=2):
    """Crop one detection (padded) and upscale, mirroring crop.py."""
    w, h = img.size
    bw, bh = det["x1"] - det["x0"], det["y1"] - det["y0"]
    x0 = max(0.0, det["x0"] - bw * pad)
    y0 = max(0.0, det["y0"] - bh * pad)
    x1 = min(1.0, det["x1"] + bw * pad)
    y1 = min(1.0, det["y1"] + bh * pad)
    box = (int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h))
    crop = img.crop(box)
    crop = crop.resize((crop.width * upscale, crop.height * upscale), Image.LANCZOS)
    crop.save(out_path)
    return out_path


def run(image_path, out_dir=CROP_DIR_DEFAULT, detections=None, use_prior=True,
        text_fusion=True):
    if detections is None:
        env = load_env()
        key = env.get("ROBOFLOW_API_KEY")
        api_url = env.get("ROBOFLOW_API_URL", DEFAULT_API_URL)
        workflow = env.get("ROBOFLOW_WORKFLOW_ID")
        model = env.get("ROBOFLOW_MODEL")
        if not key or not (workflow or model):
            sys.exit(
                "Roboflow not configured. Set ROBOFLOW_API_KEY plus either "
                "ROBOFLOW_WORKFLOW_ID (+ROBOFLOW_WORKSPACE, ROBOFLOW_CLASSES) or "
                "ROBOFLOW_MODEL (e.g. us-coins-qjnn6/1) in .env, or pass "
                "--detections <file.json> to run offline."
            )
        if workflow:  # segmentation workflow takes precedence when configured
            detections = detect_workflow(
                image_path, env.get("ROBOFLOW_WORKSPACE"), workflow,
                env.get("ROBOFLOW_CLASSES", "coin"), key, api_url,
            )
        else:
            detections = detect_roboflow(image_path, model, key, api_url)

    os.makedirs(out_dir, exist_ok=True)
    # Phone photos carry an EXIF orientation tag. Roboflow applies it (a 4032x3024
    # file with orientation=6 is reported as 3024x4032), but PIL hands back the raw
    # buffer - so cropping straight from Image.open() maps the detector's fractional
    # boxes onto a frame with width/height swapped, and every crop lands in the wrong
    # place. exif_transpose() puts us in the same frame the detector used.
    img = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")
    stem = os.path.splitext(os.path.basename(image_path))[0]
    by_denom = {}
    for d in detections:
        by_denom[d.get("raw_class") or "?"] = by_denom.get(d.get("raw_class") or "?", 0) + 1
    summary = ", ".join(f"{v} {k}" for k, v in sorted(by_denom.items()))
    print(f"{len(detections)} coin(s) detected in {os.path.basename(image_path)}"
          f"{'  (' + summary + ')' if summary else ''}\n")

    rows = []
    for i, det in enumerate(sorted(detections, key=lambda d: (d["y0"], d["x0"]))):
        out_path = os.path.join(out_dir, f"{stem}_det{i:02d}.jpg")
        crop_detection(img, det, out_path)
        denom = det.get("denomination") if use_prior else None
        top = identify(out_path, top_k=3, denomination=denom, text_fusion=text_fusion)
        best = top[0]
        rows.append((det, best, top))
        det_lbl = det.get("raw_class") or "?"
        conf = det.get("confidence", 0.0)
        print(f"[{i:02d}] detector: {det_lbl:<8} {conf:.0%}   ->   "
              f"{best['class_label']}  ({best['similarity']:.3f})")
        for r in top[1:]:
            print(f"        alt: {r['class_label']}  ({r['similarity']:.3f})")
    return rows


def main():
    args = sys.argv[1:]
    if not args:
        print("usage: python coin_detect.py <image> [out_dir] [--detections f.json] [--no-prior]")
        sys.exit(1)
    image_path = args[0]
    use_prior = "--no-prior" not in args
    text_fusion = "--no-fusion" not in args
    detections = None
    det_arg = None
    if "--detections" in args:
        det_arg = args[args.index("--detections") + 1]
        with open(det_arg) as f:
            detections = json.load(f)
    out_dir = CROP_DIR_DEFAULT
    for a in args[1:]:
        if not a.startswith("--") and a != det_arg:
            out_dir = a
            break
    run(image_path, out_dir=out_dir, detections=detections, use_prior=use_prior,
        text_fusion=text_fusion)


if __name__ == "__main__":
    main()
