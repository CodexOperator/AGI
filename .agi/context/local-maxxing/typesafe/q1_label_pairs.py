#!/usr/bin/env python3
"""q1 label ambiguity -- hypothesis:lm-jev-q1-label-is-ambiguous.
Unique (verdict, experiment) pairs joined by parents and/or evidence_runs where
both record a verdict class; two joins, suffix-stripped class compare, bootstrap
over pairs, independent-reviewed-label arm. Pure Python + numpy, zero network.
  python3 q1_label_pairs.py
"""
import glob, json, os, re, sys
from datetime import datetime, timezone
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, ".agi")):
    ROOT = os.path.dirname(ROOT)
NODES = os.path.join(ROOT, ".agi", "nodes")
CLASSES = ("inconclusive_lean_proved", "inconclusive_lean_disproved", "proved", "disproved", "pending")
def field(fm, n):
    m = re.search(r"^%s:[ \t]*(.*)$" % n, fm, re.M)
    return m.group(1).strip().strip('"') if m else None
def listfield(fm, n):
    rest = field(fm, n)
    if rest is None:
        return []
    if rest.startswith("["):
        return [x.strip().strip('"') for x in rest.strip("[]").split(",") if x.strip()]
    if rest:
        return [rest.strip('"')]
    b = re.search(r"^%s:[ \t]*\n((?:[ \t]+-[ \t]*.+\n?)*)" % n, fm, re.M)
    return [l.strip()[2:].strip().strip('"') for l in b.group(1).splitlines()] if b else []
def cls(raw):
    """Class extraction: strip the :N confidence suffix BEFORE comparing."""
    if raw is None:
        return None, "missing_field"
    v = raw.strip().lower()
    for c in CLASSES:
        if v.startswith(c):
            return c, None
    return (None, "empty_string") if v == "" else ((None, "chain_arrow_string") if "\u2192" in raw else (None, "prose_string"))
def load(rel):
    out, nc = {}, {}
    for fn in sorted(glob.glob(os.path.join(NODES, rel, "*.md"))):
        t = open(fn, encoding="utf-8", errors="replace").read()
        m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n", t, re.S)
        fm = m.group(1) if m else ""
        nid = field(fm, "id") or os.path.basename(fn)[:-3]
        c, why = cls(field(fm, "verdict"))
        out[nid] = {"id": nid, "class": c, "raw": field(fm, "verdict"), "demoted_from": field(fm, "demoted_from"),
                    "parents": listfield(fm, "parents"), "evidence_runs": listfield(fm, "evidence_runs")}
        if c is None:
            nc[why] = nc.get(why, 0) + 1
    return out, nc
def join(vd, ex, inc_ev, prefixes):
    """Unique pairs. inc_ev=0 parents only; 1 union evidence_runs."""
    seen, pairs = set(), []
    for v in vd.values():
        if v["class"] is None:
            continue
        refs = list(v["parents"]) + (list(v["evidence_runs"]) if inc_ev else [])
        for r in refs:
            if (v["id"], r) in seen or not r.startswith(prefixes):
                continue
            if r in ex and ex[r]["class"] is not None:
                seen.add((v["id"], r))
                pairs.append({"verdict": v["id"], "experiment": r, "vc": v["class"], "ec": ex[r]["class"],
                              "vraw": v["raw"], "eraw": ex[r]["raw"], "vdem": v["demoted_from"], "edem": ex[r]["demoted_from"]})
    return pairs
def boot(pairs, n=1000, seed=20260918):
    d = np.array([p["vc"] != p["ec"] for p in pairs], float)
    if not len(d):
        return None
    rng = np.random.default_rng(seed)
    rates = sorted(float(d[rng.integers(0, len(d), len(d))].mean()) for _ in range(n))
    return {"n": len(d), "rate": float(d.mean()), "lo": float(np.percentile(rates, 2.5)), "hi": float(np.percentile(rates, 97.5))}
def report(pairs):
    conf, expl = {}, 0
    for p in pairs:
        k = "%s -> %s" % (p["vc"], p["ec"])
        conf[k] = conf.get(k, 0) + 1
        if p["vc"] != p["ec"] and ((p["vdem"] and cls(p["vdem"])[0] == p["ec"]) or (p["edem"] and cls(p["edem"])[0] == p["vc"])):
            expl += 1
    b = boot(pairs)
    return {"pairs": len(pairs), "agree": sum(p["vc"] == p["ec"] for p in pairs), "disagree": sum(p["vc"] != p["ec"] for p in pairs),
            "rate": round(b["rate"], 4) if b else None, "raw_string_disagree": sum(p["vraw"] != p["eraw"] for p in pairs),
            "confusion": conf, "disagreements_explained_by_demoted_from": expl, "bootstrap": b,
            "falsifier_ci_excludes_0.15": bool(b and not (b["lo"] <= 0.15 <= b["hi"])),
            "falsifier_lo_above_0.05": bool(b and b["lo"] > 0.05)}
def scope(kind):
    recs, nc = load(kind)
    drecs, dnc = load("deprecated/" + kind)
    return recs, {"live_glob": ".agi/nodes/%s/*.md" % kind, "deprecated_glob": ".agi/nodes/deprecated/%s/*.md" % kind,
                  "live_files": len(recs), "live_with_verdict_field": sum(r["raw"] is not None for r in recs.values()),
                  "deprecated_files": len(drecs), "deprecated_with_verdict_field": sum(r["raw"] is not None for r in drecs.values()),
                  "deprecated_included": False, "nonclass_live_by_name": nc, "nonclass_deprecated_by_name": dnc}
def main():
    out = {"utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"), "scope": {}, "joins": {}, "arms": {}}
    vd, s = scope("verdict")
    ex, s2 = scope("experiment")
    out["scope"] = {"verdict": s, "experiment": s2}
    both = ("experiment:", "exp:")
    for arm, inc, pref in (("parents_only", 0, both), ("parents_union_evidence", 1, both),
                           ("parents_union_evidence_experiment_prefix_only", 1, ("experiment:",))):
        out["joins"][arm] = report(join(vd, ex, inc, pref))
    out["arms"]["reviewed_label"] = {
        "inspected_live_nodes": len(vd) + len(ex),
        "candidate_fields_found": {"demoted_from": sum(r["demoted_from"] not in (None, "0", "") for r in list(vd.values()) + list(ex.values()))},
        "verdict": "BLOCKED:no_reviewed_label",
        "why": "demoted_from is a machine transition derived from the same verdict word (season.py evidence_runs gate), "
               "not an independent reviewed verdict of the experiment; no review/reviewed_by field on any verdict node"}
    os.makedirs(os.path.join(HERE, "bench"), exist_ok=True)
    with open(os.path.join(HERE, "bench", out["utc"] + ".jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(out) + "\n")
    print(json.dumps(out, indent=2))
if __name__ == "__main__":
    sys.exit(main())