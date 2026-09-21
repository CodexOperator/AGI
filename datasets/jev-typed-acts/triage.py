#!/usr/bin/env python3
"""TM.59 review-TRIAGE (q2): ONE scrubbed jev verdict-class call per act, corrected-partition
5-feature LR accept score as an ORDERING HINT. It never decides; a reviewer/gate does.
  python3 triage.py <node-path> ...              live (cached; reruns make 0 calls)
  python3 triage.py --dry-run [<node-path> ...]  no network: TM.51 held-out rows, or cached rows"""
import hashlib, json, os, re, sys
import numpy as np
import acts_replay as J, acts_replay_scrub as S, corrected_partition_review_call as CP
HERE = os.path.dirname(os.path.abspath(__file__))
CL, WEIGHTS, CACHE = CP.CL, os.path.join(HERE, "triage_weights.json"), os.path.join(HERE, "json_cache_triage")

def feats(p):
    return np.array([float((p or {}).get(k, 0.0)) for k in CL])

def p_accept(w, p):
    return float(1.0 / (1.0 + np.exp(-(float(np.dot(w["coef"], feats(p))) + w["intercept"]))))

def flag(w, pa):
    t = w["threshold"]
    return "accept" if pa >= t + w["margin"] else ("demote" if pa <= t - w["margin"] else "uncertain")

def read_act(path):
    t = open(path, encoding="utf-8", errors="replace").read()
    m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n", t, re.S)
    fm, body = (m.group(1), t[m.end():]) if m else ("", t)
    return (J.field(fm, "id") or path), body

def get(act, body, dry):
    cp = os.path.join(CACHE, hashlib.sha256(act.encode()).hexdigest()[:24] + ".json")
    if os.path.exists(cp):
        return json.load(open(cp))["answers"], 0
    if dry:
        return {}, 0
    key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_KEY")
    if not key:
        raise SystemExit("blocked:no_key -- 0 network calls")
    st, pl, _ = J.ask(key, S.scrub(body)[0])
    ans = (pl or {}).get("answers") or {}
    tok = ((pl or {}).get("usage") or {}).get("input_tokens") or 0
    os.makedirs(CACHE, exist_ok=True)
    json.dump({"act": act, "http_status": st, "answers": ans, "input_tokens": tok}, open(cp, "w", encoding="utf-8"))
    return ans, tok

def row(act, ans, w):
    p = (ans.get("q1") or {}).get("probabilities") or {}
    pa = p_accept(w, p) if p else 0.0
    return {"act": act, "p_accept": round(pa, 4), "flag": flag(w, pa) if p else "uncertain",
            "features": {k: round(float(p.get(k, 0.0)), 6) for k in CL}}

def tm51():
    acts, by, y, kv = CP.load()
    X = np.array([np.mean([[p[k] for k in CL] for p in by[a]], axis=0) for a in acts])
    s = np.array([np.mean([sum(p[k] for k in CP.PARTS["B_corrected"]) for p in by[a]]) for a in acts])
    z = np.zeros(len(y))
    for nm, ft in (("B_corrected mapping", None), ("LR (5 probs) thr=0.5", X)):
        for pop, m in (("all", np.ones(len(y), bool)), ("verdict", kv)):
            yield (nm, pop, CP.cv(s[m], y[m]) if ft is None else CP.cv(z[m], y[m], ft[m]))

def main():
    dry, args = "--dry-run" in sys.argv, [a for a in sys.argv[1:] if not a.startswith("--")]
    w = json.load(open(WEIGHTS))
    if dry and not args:
        for nm, pop, r in tm51():
            print("%s | %s | AUC %.4f | agreement %.4f" % (nm, pop, r["auc"], r["agree"]))
    spent = 0.0
    for a in args:
        act, body = read_act(a)
        ans, tok = get(act, body, dry)
        spent += tok * J.PRICE
        print(json.dumps(row(act, ans, w), ensure_ascii=False))
    if not dry and args:
        print("TypeSafe spend: $%.6f = %d input tokens x $0.042/Mtok" % (spent, round(spent / J.PRICE)))

if __name__ == "__main__":
    main()
