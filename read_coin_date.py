"""
Read the date and mintmark off a cropped coin image.

Why a vision model and not OCR: coin dates are raised metal on a curved,
reflective, often-worn surface, at whatever rotation the coin happened to land.
Tesseract returns nothing at all on these crops; Apple's Vision framework reads
the legends ("IN GOD WE TRUST") but garbles the small date digits. A VLM reads
them the way a person does.

The date is the piece everything else in the project hangs on:
  - wheat cent (1909-1958) vs Memorial cent is a *reverse* distinction, so an
    obverse photo can't settle it - but the date can;
  - a 1964 Kennedy half is 90% silver, 1965-1970 is 40% silver, 1971+ is clad;
  - rare_flags.py and mintage_data.py are both keyed on (year, mintmark).

Output feeds straight into rare_flags.flag().

Config (.env, gitignored):
    ANTHROPIC_API_KEY=...
Usage:
    python read_coin_date.py <crop.jpg> [more.jpg ...]     # direct, one call each
    python read_coin_date.py --batch <dir>                 # Batch API, 50% cheaper
"""
import base64
import json
import os
import sys
import time

import anthropic

from coin_detect import load_env

MODEL = "claude-opus-4-8"
MAX_EDGE = 1568          # above this the API downsizes anyway; sending more just costs tokens

PROMPT = """You are reading a single U.S. coin from a photograph.

Report ONLY what you can actually see. A wrong date is worse than no date: a
1969 Kennedy half is 40% silver while a 1971 is worthless clad, so a guess that
looks confident does real damage.

- year: the 4-digit date, or null if you cannot read it with confidence.
- mint_mark: the small letter near the date - D (Denver), S (San Francisco),
  P (Philadelphia), W (West Point), CC (Carson City). Philadelphia coins often
  carry NO mintmark at all; report "P" only if you can see the letter, use
  "none" when you can see the spot where a mintmark would be and it is bare,
  and "unknown" when you simply cannot tell.
- The coin may be rotated, upside down, worn, or toned. Read it anyway.
"""

# NB: the structured-outputs validator rejects an `enum` on a union type
# (["string","null"]), so mint_mark carries an explicit "unknown" member rather
# than allowing null.
SCHEMA = {
    "type": "object",
    "properties": {
        "year": {"type": ["integer", "null"], "description": "4-digit year, or null if not legible"},
        "mint_mark": {"type": "string", "enum": ["D", "S", "P", "W", "CC", "none", "unknown"],
                      "description": "mintmark letter; 'none' if visibly absent, 'unknown' if unreadable"},
        "side": {"type": "string", "enum": ["obverse", "reverse", "unclear"]},
        "denomination": {"type": "string",
                         "description": "cent, nickel, dime, quarter, half dollar, dollar, or unknown"},
        "series": {"type": "string", "description": "e.g. Lincoln Memorial cent, Kennedy Half Dollar"},
        "confidence": {"type": "string", "enum": ["high", "medium", "low"]},
        "notes": {"type": "string", "description": "anything odd - doubling, damage, unusual toning"},
    },
    "required": ["year", "mint_mark", "side", "denomination", "series", "confidence", "notes"],
    "additionalProperties": False,
}


def _encode(path):
    """Downscale to the API's effective ceiling before encoding - a 4000px crop
    costs the same tokens as a 1568px one, so the extra bytes buy nothing."""
    from PIL import Image, ImageOps
    img = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    if max(img.size) > MAX_EDGE:
        img.thumbnail((MAX_EDGE, MAX_EDGE), Image.LANCZOS)
    import io
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.standard_b64encode(buf.getvalue()).decode()


def _content(path):
    return [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": _encode(path)}},
        {"type": "text", "text": PROMPT},
    ]


def _client():
    env = load_env()
    key = env.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit("No ANTHROPIC_API_KEY. Add it to .env (gitignored) and re-run.")
    return anthropic.Anthropic(api_key=key)


def read_one(path, client=None):
    client = client or _client()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        thinking={"type": "adaptive"},
        output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[{"role": "user", "content": _content(path)}],
    )
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text)


def read_batch(paths, client=None, poll=20):
    """Batch API: same requests at 50% cost. Worth it for a whole bag of coins."""
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    client = client or _client()
    requests = [
        Request(
            custom_id=f"coin-{i:04d}",
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=2000,
                thinking={"type": "adaptive"},
                output_config={"effort": "medium", "format": {"type": "json_schema", "schema": SCHEMA}},
                messages=[{"role": "user", "content": _content(p)}],
            ),
        )
        for i, p in enumerate(paths)
    ]
    batch = client.messages.batches.create(requests=requests)
    print(f"batch {batch.id}: {len(requests)} coins submitted")

    while True:
        batch = client.messages.batches.retrieve(batch.id)
        if batch.processing_status == "ended":
            break
        print(f"  {batch.processing_status}... ({batch.request_counts.processing} in flight)")
        time.sleep(poll)

    # results come back in arbitrary order - key by custom_id, never by position
    by_id = {}
    for result in client.messages.batches.results(batch.id):
        if result.result.type != "succeeded":
            by_id[result.custom_id] = {"error": result.result.type}
            continue
        msg = result.result.message
        text = next((b.text for b in msg.content if b.type == "text"), "{}")
        by_id[result.custom_id] = json.loads(text)
    return [by_id.get(f"coin-{i:04d}", {"error": "missing"}) for i in range(len(paths))]


def _report(path, r):
    if "error" in r:
        print(f"{os.path.basename(path):<24} ERROR {r['error']}")
        return
    mm = r.get("mint_mark")
    known = mm not in (None, "none", "unknown")
    date = f"{r['year']}-{mm}" if r.get("year") and known else str(r.get("year") or "????")
    print(f"{os.path.basename(path):<24}{date:<10}{r.get('series','')[:30]:<32}{r.get('confidence','')}")
    # hand it to the flagger. "none" = Philadelphia (no mintmark struck); "unknown"
    # means we couldn't read it, which is what the check-the-mintmark rule is for.
    from rare_flags import flag
    hit, why = flag({
        "year": r.get("year"),
        "mint_mark": "P" if mm == "none" else (mm if known else "not legible in photo"),
        "design_variety": r.get("series", ""),
        "denomination": r.get("denomination", ""),
        "category": f"Circulating {r.get('denomination','').title()}",
        "wheat_reverse": "wheat" in r.get("series", "").lower(),
    })
    if hit:
        print(f"    FLAG: {why}")


def main():
    args = [a for a in sys.argv[1:] if a != "--batch"]
    if not args:
        print("usage: python read_coin_date.py <crop.jpg> ... | --batch <dir>")
        sys.exit(1)

    if "--batch" in sys.argv:
        import glob
        paths = sorted(
            p for d in args for p in glob.glob(os.path.join(d, "*"))
            if p.lower().endswith((".jpg", ".jpeg", ".png"))
        )
        results = read_batch(paths)
    else:
        client = _client()
        paths, results = args, [read_one(p, client) for p in args]

    print(f"\n{'image':<24}{'date':<10}{'series':<32}conf")
    print("-" * 74)
    for p, r in zip(paths, results):
        _report(p, r)


if __name__ == "__main__":
    main()
