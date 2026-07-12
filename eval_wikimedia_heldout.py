"""
Held-out accuracy test for the coin identifier using Wikimedia Commons photos.

Commons coin categories give ground-truth labels for free, and none of these
specific images are in our reference gallery, so this is a genuine held-out
test (unlike testing on the HF/Kaggle sets that were folded in). Downloads a
handful of images per class into a local cache dir (not committed), runs the
existing identify() top-1 rule, and reports per-class + overall accuracy.

Usage: python eval_wikimedia_heldout.py [images_per_class]
"""
import os
import sys
import time
import json
import urllib.parse
import urllib.request
import collections

from identify_coin import identify

API = "https://commons.wikimedia.org/w/api.php"
UA = "CoinIDHeldoutTest/1.0 (research; contact ajassovlsf@gmail.com)"
TEST_ROOT = os.path.expanduser("~/.cache/kaggle_coin_datasets/wikimedia_heldout")

# class -> (candidate Commons categories, keyword expected in predicted class_label)
CLASSES = {
    "Lincoln Cent":            (["Lincoln cents", "Lincoln cent"], "Lincoln"),
    "Jefferson Nickel":        (["Jefferson nickel", "Jefferson nickels"], "Jefferson"),
    "Roosevelt Dime":          (["Roosevelt dimes", "Roosevelt dime"], "Roosevelt"),
    "Washington Quarter":      (["Washington quarter", "Washington quarters"], "Washington"),
    "Franklin Half Dollar":    (["Franklin half dollar"], "Franklin"),
    "Kennedy Half Dollar":     (["Kennedy half dollar"], "Kennedy"),
    "Eisenhower Dollar":       (["Eisenhower dollar"], "Eisenhower"),
    "Susan B. Anthony Dollar": (["Susan B. Anthony dollar"], "Susan"),
    "Morgan Dollar":           (["Morgan dollar"], "Morgan"),
    "Peace Dollar":            (["Peace dollar"], "Peace"),
}

IMG_EXTS = (".jpg", ".jpeg", ".png")


def _get(params):
    params = dict(params, format="json")
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def category_files(category, want):
    """Return up to `want` file titles from a category (direct files first,
    then one level of subcategories if needed)."""
    titles, subcats = [], []
    cont = {}
    while len(titles) < want:
        data = _get({
            "action": "query", "list": "categorymembers",
            "cmtitle": f"Category:{category}", "cmlimit": "100", **cont,
        })
        for m in data.get("query", {}).get("categorymembers", []):
            ns, title = m["ns"], m["title"]
            if ns == 6 and title.lower().endswith(IMG_EXTS):
                titles.append(title)
            elif ns == 14:
                subcats.append(title.split(":", 1)[1])
        cont = data.get("continue", {})
        if not cont:
            break
    for sc in subcats:
        if len(titles) >= want:
            break
        try:
            data = _get({
                "action": "query", "list": "categorymembers",
                "cmtitle": f"Category:{sc}", "cmtype": "file", "cmlimit": "50",
            })
            for m in data.get("query", {}).get("categorymembers", []):
                if m["title"].lower().endswith(IMG_EXTS):
                    titles.append(m["title"])
        except Exception:
            pass
    return titles[:want]


def thumb_urls(titles, width=500):
    urls = {}
    for i in range(0, len(titles), 40):
        batch = titles[i:i + 40]
        data = _get({
            "action": "query", "prop": "imageinfo", "iiprop": "url",
            "iiurlwidth": str(width), "titles": "|".join(batch),
        })
        for p in data.get("query", {}).get("pages", {}).values():
            ii = p.get("imageinfo")
            if ii:
                urls[p["title"]] = ii[0].get("thumburl") or ii[0].get("url")
    return urls


def download(url, dest, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 1000:  # render not ready / empty
                raise IOError("too small")
            with open(dest, "wb") as f:
                f.write(data)
            return True
        except Exception:
            time.sleep(1.0 + attempt)
    return False


def fetch_class(cls, cats, per_class):
    outdir = os.path.join(TEST_ROOT, cls.replace(" ", "_").replace(".", ""))
    os.makedirs(outdir, exist_ok=True)
    titles = []
    for cat in cats:
        titles = category_files(cat, per_class * 5)  # over-fetch, some may fail
        if titles:
            break
    if not titles:
        return outdir, 0
    urls = thumb_urls(titles)
    got = 0
    for t in titles:
        if got >= per_class:
            break
        u = urls.get(t)
        if not u:
            continue
        ext = os.path.splitext(u)[1].lower()
        if ext not in IMG_EXTS:
            ext = ".jpg"
        dest = os.path.join(outdir, f"{got:02d}{ext}")
        if download(u, dest):
            got += 1
            time.sleep(0.3)
    return outdir, got


def main():
    per_class = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"Fetching ~{per_class}/class from Wikimedia Commons into {TEST_ROOT}\n")
    per_cls_dir = {}
    for cls, (cats, _kw) in CLASSES.items():
        d, n = fetch_class(cls, cats, per_class)
        per_cls_dir[cls] = d
        print(f"  {cls:<26} {n} images")

    print("\nEvaluating (top-1 nearest neighbor)...\n")
    print(f"{'class':<26}{'n':>3}  {'top1':>5}  {'acc':>5}   common confusions")
    print("-" * 78)
    total_ok = total_n = 0
    for cls, (_cats, kw) in CLASSES.items():
        d = per_cls_dir[cls]
        imgs = [os.path.join(d, f) for f in sorted(os.listdir(d))
                if f.lower().endswith(IMG_EXTS)] if os.path.isdir(d) else []
        ok = 0
        wrong = collections.Counter()
        for img in imgs:
            try:
                pred = identify(img, top_k=1)[0]["class_label"]
            except Exception:
                continue
            if kw.lower() in pred.lower():
                ok += 1
            else:
                wrong[pred] += 1
        n = len(imgs)
        total_ok += ok
        total_n += n
        acc = f"{ok/n:.0%}" if n else "-"
        conf = ", ".join(f"{c}×{k}" for k, c in wrong.most_common(3))
        print(f"{cls:<26}{n:>3}  {ok:>5}  {acc:>5}   {conf}")
    print("-" * 78)
    if total_n:
        print(f"{'OVERALL':<26}{total_n:>3}  {total_ok:>5}  {total_ok/total_n:>5.0%}")


if __name__ == "__main__":
    main()
