#!/usr/bin/env python3
"""Is the surviving jev q1 gap composition? -- experiment:a00-90f2ccea-924fef.

Reads the PINNED 370-act ECHO corpus (acts_replay_scrub.jsonl, arm [SCRUBBED])
and scores it against a body-blind per-KIND majority prior, so a reader can see
global base / kind-aware prior / jev side by side. No network, no model calls.

  python3 jev_residual_composition.py
"""
import json, os, random, sys
from datetime import datetime, timezone
import acts_replay_scrub as S

HERE = os.path.dirname(os.path.abspath(__file__))
BENCH, SEED, B = os.path.join(HERE, "bench"), 20260918, 1000


def majority_of(vals):
    return max(set(vals), key=vals.count) if vals else None


def score(acts):
    """Pure. acts: [{id,kind,label,jev_choice}]. Raises on empty."""
    if not acts:
        raise ValueError("empty corpus -- undefined, refusing to score")
    labs = [a["label"] for a in acts]
    glob = majority_of(labs)
    kinds = {}
    for a in acts:
        kinds.setdefault(a["kind"], []).append(a)
    prior = {k: majority_of([a["label"] for a in g]) for k, g in kinds.items()}
    out = {"n": len(acts), "global_choice": glob,
           "global_acc": sum(l == glob for l in labs) / len(acts),
           "prior_choice": prior,
           "prior_acc": sum(a["label"] == prior[a["kind"]] for a in acts) / len(acts),
           "jev_acc": sum(a["jev_choice"] == a["label"] for a in acts) / len(acts),
           "per_kind": {}}
    for k, g in kinds.items():
        out["per_kind"][k] = {
            "n": len(g), "prior_choice": prior[k],
            "prior_acc": sum(a["label"] == prior[k] for a in g) / len(g),
            "jev_acc": sum(a["jev_choice"] == a["label"] for a in g) / len(g),
            "global_acc": sum(a["label"] == glob for a in g) / len(g)}
    return out


def boot(pairs, rng):
    n, ds = len(pairs), []
    for _ in range(B):
        s = [pairs[rng.randrange(n)] for _ in range(n)]
        ds.append(sum(p[0] for p in s) / n - sum(p[1] for p in s) / n)
    ds.sort()
    return ds[max(0, int(0.025 * B))], ds[min(B - 1, int(0.975 * B))]


def build():
    acts, by = [], S.group([json.loads(l) for l in open(S.SCRUB_ROWS, encoding="utf-8")
                            if json.loads(l)["arm"] == S.PLACEHOLDER])
    for a in S.pinned_corpus():
        rs, lab = by.get(a["id"]), a["labels"].get("q1")
        if not rs or lab is None:
            continue
        acts.append({"id": a["id"], "kind": a["kind"], "label": lab,
                     "jev_choice": S.majority(rs, "q1"), "jev_first": rs[0]["answers"]["q1"]["choice"]})
    return acts, by


def main():
    acts, by = build()
    r = score(acts)
    rng = random.Random(SEED)
    pairs = [(a["jev_choice"] == a["label"], a["label"] == r["prior_choice"][a["kind"]]) for a in acts]
    pooled = boot(pairs, rng)
    per = {k: boot([(a["jev_choice"] == a["label"], a["label"] == r["per_kind"][k]["prior_choice"])
                    for a in acts if a["kind"] == k], rng) for k in r["per_kind"]}
    os.makedirs(BENCH, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = os.path.join(BENCH, stamp + ".jsonl")
    with open(path, "w", encoding="utf-8") as fh:
        for a in acts:
            fh.write(json.dumps({"act": a["id"], "kind": a["kind"], "label": a["label"],
                                 "jev_choice": a["jev_choice"], "prior_choice": r["prior_choice"][a["kind"]],
                                 "jev_ok": a["jev_choice"] == a["label"],
                                 "prior_ok": a["label"] == r["prior_choice"][a["kind"]]}) + "\n")
    canonical = {k: S.agree({i: v for i, v in by.items() if v[0]["kind"] == k}, "q1")
                 for k in ("verdict", "experiment")}
    canonical["pooled"] = S.agree(by, "q1")
    lines = ["# jev_residual_composition", "",
             "SEED=%d BOOTSTRAP=%d pooled_n=%d rows=%s" % (SEED, B, r["n"], os.path.basename(path)), "",
             "| scope | n | global base | kind prior | jev (majority3) | jev (first repeat) | jev-prior (95%% CI) |",
             "|---|---|---|---|---|---|---|",
             "| pooled | %d | %.3f (`%s`) | %.3f | %.3f | %.3f | %+.3f [%+.3f, %+.3f] |" % (
                 r["n"], r["global_acc"], r["global_choice"], r["prior_acc"], r["jev_acc"],
                 sum(a["jev_first"] == a["label"] for a in acts) / len(acts), r["jev_acc"] - r["prior_acc"], pooled[0], pooled[1]),
             ]
    for k in ("verdict", "experiment"):
        pk = r["per_kind"][k]
        lines.append("| %s | %d | %.3f | %.3f (`%s`) | %.3f | %.3f | %+.3f [%+.3f, %+.3f] |" % (
            k, pk["n"], pk["global_acc"], pk["prior_acc"], pk["prior_choice"], pk["jev_acc"],
            sum(a["jev_first"] == a["label"] for a in acts if a["kind"] == k) / pk["n"],
            pk["jev_acc"] - pk["prior_acc"], per[k][0], per[k][1]))
    lines += ["", "canonical S.agree (majority3) pooled %.3f verdict %.3f experiment %.3f" % (
        canonical["pooled"][1], canonical["verdict"][1], canonical["experiment"][1]),
        "global-majority baseline `%s` = %.3f (kind-aware prior is the target claim's comparator)" % (r["global_choice"], r["global_acc"]),
        "target node quoted first-repeat 0.695 experiment / 0.479 verdict; canonical majority3 differs as tabulated.",
        "falsifier: pooled jev >= kind-aware prior -> composition claim NOT supported."]
    print("\n".join(lines))
    return 0 if pooled[1] < 0 else 1


if __name__ == "__main__":
    sys.exit(main())
