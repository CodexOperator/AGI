#!/usr/bin/env python3
"""Single-axis shape + prior control -- hypothesis:lm-jev-single-axis-question-beats-baseline: 3 arms on ONE pinned scrubbed corpus (ids from acts_replay_scrub.jsonl, labels re-derived live, state = body after acts_replay_scrub.scrub()); ONE jsonl cache (key = arm|act|repeat|model) + ONE rows jsonl, flushed per call; a cache hit replays at $0."""
import hashlib, json, os, sys, threading, urllib.request
from concurrent.futures import ThreadPoolExecutor
import acts_replay as J
import acts_replay_scrub as S
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE, ROWS, MD = (os.path.join(HERE, n) for n in ("single_axis_cache.jsonl", "single_axis_rows.jsonl", "single_axis.md"))
TOTAL_CAP, SPENT = 1.00, [0.0]
# arm1's wire key is q2 so acts_replay_scrub.agree's noul branch scores it (key names are arbitrary).
ARMS = {"arm0_prior": ("id", J.Q), "arm1_review": ("scrub", {"q2": {"type": "noul", "instructions": "Is this work accepted as-is, not demoted?"}}), "arm2_verdict": ("scrub", {"q1": {"type": "choice", "instructions": J.Q["q1"]["instructions"], "criteria": J.Q["q1"]["criteria"]}})}
SPEC = [("arm0_prior", "q1", "choice"), ("arm0_prior", "q2", "noul"), ("arm1_review", "q2", "noul"), ("arm2_verdict", "q1", "choice")]
AUC = lambda sc, pos: (lambda P, N: None if not P or not N else (sum(p > n for p in P for n in N) + 0.5 * sum(p == n for p in P for n in N)) / (len(P) * len(N)))([s for s, p in zip(sc, pos) if p], [s for s, p in zip(sc, pos) if not p])
def call(key, state, qs):
    req = urllib.request.Request(J.ENDPOINT, data=json.dumps({"state": state, "model": J.MODEL, "questions": qs}).encode(), method="POST", headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    try:
        with urllib.request.urlopen(req, timeout=120) as r: return r.status, json.loads(r.read().decode())
    except Exception as e: return getattr(e, "code", 0), {"error": str(e)}
def score(rows):
    by = {}
    for r in rows: by.setdefault((r["arm"], r["act"]), []).append(r)
    L = ["# single axis -- hypothesis:lm-jev-single-axis-question-beats-baseline", "", "MODEL=%s SEED=%d REPEATS=%d; n_acts=%d; spend $%.6f of cap $%.2f." % (J.MODEL, J.SEED, J.REPEATS, len({r["act"] for r in rows}), SPENT[0], TOTAL_CAP), "", "| arm | q | label | n | agree | base | AUC | ECE | confusion |", "|---|---|---|---|---|---|---|---|---|"]
    for arm, q, kind in SPEC:
        rby = {a: rs for (m, a), rs in by.items() if m == arm}
        n, ag, base, _ = S.agree(rby, q)
        it = []
        for a, rs in rby.items():
            lab = rs[0]["labels"].get(q)
            if lab is None: continue
            if kind == "noul":
                p = sum((r["answers"].get(q, {}).get("noul") or 0.0) for r in rs) / len(rs); d = {"accept": p, "demote": 1 - p}
            else:
                d = {}
                for r in rs:
                    for c, v in (r["answers"].get(q, {}).get("probabilities") or {}).items(): d[c] = d.get(c, 0) + v / len(rs)
            if d: it.append((lab, d))
        labs, preds = [l for l, _ in it], [max(d, key=d.get) for _, d in it]
        cs = ["accept"] if kind == "noul" else sorted(set(labs))
        As = [x for x in (AUC([d.get(c, 0.0) for _, d in it], [l == c for l in labs]) for c in cs) if x is not None]
        b, cfl = [[0, 0.0, 0] for _ in range(10)], {}
        for (lab, d), p in zip(it, preds):
            i = min(9, int(max(d.values()) * 10)); b[i][0] += 1; b[i][1] += max(d.values()); b[i][2] += p == lab; cfl[(lab, p)] = cfl.get((lab, p), 0) + 1
        t = sum(x[0] for x in b); e = sum(x[0] * abs(x[1] / x[0] - x[2] / x[0]) for x in b if x[0]) / t if t else 0.0
        L.append("| %s | %s | %s | %d | %.3f | %.3f | %s | %.3f | %s |" % (arm, q, q, n, ag, base, ("%.3f" % (sum(As) / len(As))) if As else "na", e, " ".join("%s>%s:%d" % (x, y, c) for (x, y), c in sorted(cfl.items(), key=lambda kv: -kv[1])[:6])))
    open(MD, "w", encoding="utf-8").write("\n".join(L) + "\n"); print("\n".join(L))
def main():
    key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_KEY")
    acts = S.pinned_corpus()
    scr = {a["id"]: S.scrub(a["state"])[0] for a in acts}
    leaks = {a["id"]: len(S.PAT.findall(scr[a["id"]])) for a in acts}
    print("acts=%d residual_leak_tokens=%d leaked_acts=%.3f" % (len(acts), sum(leaks.values()), sum(1 for v in leaks.values() if v) / len(acts)))
    if not key: sys.stderr.write("blocked:no_key -- 0 network calls\n"); return 2
    cache = {d["key"]: d for d in map(json.loads, open(CACHE))} if os.path.exists(CACHE) else {}
    cf, rf, lock = open(CACHE, "a", encoding="utf-8"), open(ROWS, "w", encoding="utf-8"), threading.Lock()
    def run(job):
        arm, a, rep = job
        ck = hashlib.sha256(("%s|%s|%d|%s" % (arm, a["id"], rep, J.MODEL)).encode()).hexdigest()[:24]
        if ck not in cache:
            st, pl = (0, {"blocked": "total_cap"}) if SPENT[0] >= TOTAL_CAP else call(key, a["id"] if ARMS[arm][0] == "id" else scr[a["id"]], ARMS[arm][1])
            cache[ck] = {"key": ck, "arm": arm, "act": a["id"], "repeat": rep, "model": J.MODEL, "http_status": st, "payload": pl}
            with lock:
                cf.write(json.dumps(cache[ck], ensure_ascii=False) + "\n"); cf.flush()
        d, u = cache[ck], ((cache[ck]["payload"] or {}).get("usage") or {})
        row = {"arm": arm, "act": a["id"], "kind": a["kind"], "repeat": rep, "model": (d["payload"] or {}).get("model"), "http_status": d["http_status"], "input_tokens": u.get("input_tokens"), "leak_after": leaks[a["id"]], "labels": a["labels"], "answers": (d["payload"] or {}).get("answers") or {}}
        with lock:
            rf.write(json.dumps(row, ensure_ascii=False) + "\n"); rf.flush(); SPENT[0] += (u.get("input_tokens") or 0) * J.PRICE
        return row
    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(run, [(arm, a, rep) for arm in ARMS for a in acts for rep in range(J.REPEATS)]))
    score(rows)
    print("rows=%d http200=%d spend=$%.6f" % (len(rows), sum(1 for r in rows if r["http_status"] == 200), SPENT[0]))
    return 0
if __name__ == "__main__":
    sys.exit(main())
