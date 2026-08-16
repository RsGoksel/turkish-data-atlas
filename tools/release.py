"""Cut datasets.json to a release stage.

The full catalogue lives in datasets.full.json and never shrinks. This script writes the
public datasets.json containing everything up to --stage, and records what is still
scheduled so the page can say so rather than pretend it does not exist.

    python tools/release.py --stage 1     # Konuşma
    python tools/release.py --stage 2     # + Metin / LLM
    python tools/release.py --stage 3     # + Görüntü
"""
import argparse, json, os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--stage", type=int, required=True, choices=[1, 2, 3])
ap.add_argument("--full", default=os.path.join(ROOT, "datasets.full.json"))
ap.add_argument("--out",  default=os.path.join(ROOT, "datasets.json"))
a = ap.parse_args()

full = json.load(open(a.full, encoding="utf-8"))
live = [x for x in full["datasets"] if x["release"] <= a.stage]
hf   = [x for x in live if x["host"] == "huggingface"]

meta = dict(full["meta"])
meta["stage"] = a.stage
meta["counts"] = {
    "total": len(live),
    "huggingface": len(hf),
    "external": len(live) - len(hf),
    "by_modality": dict(Counter(x["modality"] for x in live)),
    "by_posture":  dict(Counter(x["posture"]  for x in live)),
}
meta["volume"] = {
    "turkish_only_tb": round(sum(x.get("bytes") or 0 for x in hf if not x["multilingual"]) / 1e12, 2),
    "turkish_only_n":  sum(1 for x in hf if not x["multilingual"] and x.get("bytes")),
    "multilingual_all_langs_tb": round(sum(x.get("bytes") or 0 for x in hf if x["multilingual"]) / 1e12, 2),
    "multilingual_n":  sum(1 for x in hf if x["multilingual"] and x.get("bytes")),
}
# Henuz yayinlanmamis bolumler: sayfada "yakinda" olarak gorunsun.
meta["upcoming"] = [
    {"stage": s, **{k: v for k, v in r.items() if k != "modalities"}, "modalities": r["modalities"]}
    for s, r in sorted(full["meta"]["releases"].items(), key=lambda kv: int(kv[0]))
    if int(s) > a.stage
]
json.dump({"meta": meta, "datasets": live}, open(a.out, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"stage {a.stage}: {len(live)} live, {len(full['datasets']) - len(live)} scheduled")
print(" ", meta["counts"]["by_modality"], "|", meta["volume"]["turkish_only_tb"], "TB")
