"""Cut datasets.json to a release stage.

The full verified catalogue lives in datasets.full.json and never shrinks; each record
carries a release stage. This script writes the public datasets.json containing every
record up to --stage, recomputing counts and volumes for exactly what is shown.

    python tools/release.py --stage 1
    python tools/release.py --stage 2
    python tools/release.py --stage 3
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

meta = {k: v for k, v in full["meta"].items() if k not in ("releases", "upcoming")}
meta["version"] = f"v{a.stage}"
meta["counts"] = {
    "total": len(live),
    "huggingface": len(hf),
    "external": len(live) - len(hf),
    "by_modality": dict(Counter(x["modality"] for x in live)),
    "by_posture":  dict(Counter(x["posture"]  for x in live)),
}
def vol(status):
    sel = [x for x in hf if x["lang_status"] == status and x.get("bytes")]
    return len(sel), round(sum(x["bytes"] for x in sel) / 1e12, 2)

n_tr, tb_tr = vol("tr")          # dil etiketi yalnizca tr
n_un, tb_un = vol("untagged")    # dil etiketi hic yok
n_ml, tb_ml = vol("multi")       # cokdilli; hacim TUM dillerin
meta["volume"] = {
    "turkish_only_tb": tb_tr, "turkish_only_n": n_tr,
    "untagged_tb": tb_un, "untagged_n": n_un,
    "multilingual_all_langs_tb": tb_ml, "multilingual_n": n_ml,
}
json.dump({"meta": meta, "datasets": live}, open(a.out, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(f"{meta['version']}: {len(live)} kayit")
print(" ", meta["counts"]["by_modality"], "|", meta["volume"]["turkish_only_tb"], "TB")
