#!/usr/bin/env python3
"""Held-out typed-acts replay -- hypothesis:lm-jev-typed-acts-replay.

170 verdict nodes + 200 seed-sampled experiment nodes (only those carrying a
recorded verdict). State = the node BODY only, frontmatter stripped so no
recorded label leaks. ONE jev-1.13.0 request per act carries all five
questions. Every response is cached as json under json_cache/ so the analysis
re-runs at $0; every row is appended to acts_replay.jsonl as it is produced.
Reads TYPESAFE_API_KEY (else TYPESAFE_KEY) from os.environ at call time; with
no key it makes ZERO network calls and exits 2.

  python3 acts_replay.py         # replay + score + write acts_replay.md
  python3 acts_replay.py --dry   # corpus only, no network
"""
import hashlib, json, os, random, re, sys, time, urllib.error, urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, ".agi")):
    ROOT = os.path.dirname(ROOT)
NODES = os.path.join(ROOT, ".agi", "nodes")
CACHE, ROWS, MD = (os.path.join(HERE, n) for n in ("json_cache", "acts_replay.jsonl", "acts_replay.md"))
ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL, SEED, REPEATS, PRICE, CAP = "jev-1.13.0", 20260918, 3, 0.042 / 1e6, 0.50
VERDICTS = ["proved", "disproved", "inconclusive_lean_proved", "inconclusive_lean_disproved", "pending"]
Q = {
 "q1": {"type": "choice", "instructions": "Select the verdict class this node records.",
        "criteria": {"proved": "a verdict of proved", "disproved": "a verdict of disproved",
                     "inconclusive_lean_proved": "leans proved, not conclusive",
                     "inconclusive_lean_disproved": "leans disproved, not conclusive", "pending": "no verdict"}},
 "q2": {"type": "noul", "instructions": "Is this work accepted as-is, not demoted?"},
 "q3": {"type": "noul", "instructions": "Does this act cut the work short (ask for a re-brief) instead of proceeding?"},
 "q4": {"type": "choice", "instructions": "Is the change big or small?",
        "criteria": {"big": "production lines exceed the ceiling", "small": "at or under the ceiling"}},
 "q5": {"type": "noul", "instructions": "Is the spawn shape of this node legal under its schema?"},
}


def field(t, n):
    m = re.search(r"^%s:[ \t]*(.*)$" % n, t, re.M)
    return m.group(1).strip().strip('"') if m else ""


def norm(v):
    v = v.strip().lower()
    return next((w for w in VERDICTS if v.startswith(w)), "")


def records():
    out = []
    for kind, cap in (("verdict", 0), ("experiment", 200)):
        d = os.path.join(NODES, kind)
        fs = sorted(f for f in os.listdir(d) if f.endswith(".md"))
        if cap:
            random.Random(SEED).shuffle(fs)
        taken = 0
        for fn in fs:
            t = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read()
            m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n", t, re.S)
            fm, body = (m.group(1), t[m.end():]) if m else ("", t)
            v = norm(field(fm, "verdict"))
            if kind == "experiment" and not v:
                continue
            lab = {"q2": "demote" if field(fm, "demoted_from") else "accept",
                   "q3": "cut" if field(fm, "rebrief_request") else "proceed"}
            if v:
                lab["q1"] = v
            pl, lc = field(fm, "production_lines"), field(fm, "line_ceiling")
            if pl.isdigit() and lc.isdigit():
                lab["q4"] = "big" if int(pl) > int(lc) else "small"
            out.append({"id": field(fm, "id") or kind + ":" + fn[:-3], "kind": kind,
                        "state": body[:128000], "labels": lab})
            taken += 1
            if cap and taken >= cap:
                break
    return out


def ask(key, state):
    body = json.dumps({"state": state, "model": MODEL, "questions": Q}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return r.status, json.loads(r.read().decode()), time.time() - t0
    except urllib.error.HTTPError as e:
        return e.code, None, time.time() - t0
    except Exception as e:
        return 0, {"error": str(e)}, time.time() - t0


def pick(row, q):
    a = row["answers"].get(q) or {}
    if q in ("q1", "q4"):
        p = a.get("probabilities") or {}
        return (max(p, key=p.get) if p else None), a.get("confidence")
    v = a.get("noul")
    if v is None:
        return None, None
    hi = {"q2": "accept", "q3": "cut", "q5": "legal"}[q]
    lo = {"q2": "demote", "q3": "proceed", "q5": "illegal"}[q]
    return (hi if v > 0.5 else lo), (v if v > 0.5 else 1 - v)


def score(acts, rows, spent):
    by = {}
    for r in rows:
        by.setdefault(r["act"], []).append(r)
    md = ["# acts_replay -- hypothesis:lm-jev-typed-acts-replay", "",
          "MODEL=%s (pinned); SEED=%d; REPEATS=%d; state = node BODY only, frontmatter stripped, cap 128k chars." % (MODEL, SEED, REPEATS),
          "Corpus: %d acts = %d verdict + %d experiment." % (len(acts), sum(a["kind"] == "verdict" for a in acts), sum(a["kind"] == "experiment" for a in acts)),
          "", "| question | recorded | agree | base | repeat-flip | ECE |", "|---|---|---|---|---|---|"]
    for q in Q:
        n = ok = flips = 0
        bins = [[0, 0.0, 0.0] for _ in range(10)]
        labs = []
        for rs in by.values():
            lab = rs[0]["labels"].get(q)
            if lab is None:
                continue
            got = [(pick(r, q)[0], pick(r, q)[1]) for r in rs]
            ps = [g[0] for g in got if g[0]]
            if not ps:
                continue
            n += 1
            labs.append(lab)
            ok += max(set(ps), key=ps.count) == lab
            flips += len(set(ps)) > 1
            for p, c in got:
                if p is None or c is None:
                    continue
                b = min(9, int(c * 10))
                bins[b][0] += 1
                bins[b][1] += c
                bins[b][2] += (p == lab)
        tot = sum(b[0] for b in bins)
        ece = sum(b[0] * abs(b[1] / b[0] - b[2] / b[0]) for b in bins if b[0]) / tot if tot else 0
        base = max(labs.count(x) for x in set(labs)) / len(labs) if labs else 0
        md.append("| %s | %d | %.3f | %.3f | %.3f | %.3f |" % (q, n, ok / n if n else 0, base, flips / n if n else 0, ece))
    md += ["", "TypeSafe spend: $%.6f = %d input tokens x $0.042/Mtok (cap $%.2f; output free per trove)." % (spent["usd"], round(spent["usd"] / PRICE), CAP),
           "TYPESAFE_KEY len omitted; endpoint %s; no host/model/key id written." % ENDPOINT,
           "", "## Data gates (named, not padded)", "",
           "- merge-up-review.jsonl does not exist on this box; review decisions are not a structured corpus (only ~15 accept_with_residue occurrences across all rotation records). Rows here carry accept/demote labels derived from the recorded `demoted_from` field instead.",
           "- rebrief answers: only 8-10 nodes carry `rebrief_request` in this checkout, not 50; q3 is scored on those records.",
           "- Creation timestamps are absent from node files and `mtime` is uniform after checkout; `git log` is forbidden by the kid contract, so held-out is a seeded draw over the whole live corpus (seed above) rather than a literal post-2026-09-15 cut.",
           ""]
    open(MD, "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))


def main():
    dry = "--dry" in sys.argv
    key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_KEY")
    acts = records()
    print("acts=%d verdict=%d experiment=%d" % (len(acts), sum(a["kind"] == "verdict" for a in acts), sum(a["kind"] == "experiment" for a in acts)))
    if dry or not key:
        sys.stderr.write("blocked:%s -- 0 network calls\n" % ("dry_run" if dry else "no_key"))
        return 2
    os.makedirs(CACHE, exist_ok=True)
    fh = open(ROWS, "w", encoding="utf-8")
    spent = {"usd": 0.0}
    lock = __import__("threading").Lock()

    def run(job):
        a, r = job
        ck = hashlib.sha256(("%s|%d|%s" % (a["id"], r, MODEL)).encode()).hexdigest()[:24]
        cp = os.path.join(CACHE, ck + ".json")
        if os.path.exists(cp):
            d = json.load(open(cp))
            st, pl, dt = d["http_status"], d["payload"], d["latency_s"]
        elif spent["usd"] >= CAP:
            st, pl, dt = 0, {"blocked": "budget_cap"}, 0.0
        else:
            st, pl, dt = ask(key, a["state"])
            json.dump({"act": a["id"], "repeat": r, "model": MODEL, "http_status": st,
                       "latency_s": round(dt, 4), "payload": pl},
                      open(cp, "w", encoding="utf-8"), ensure_ascii=False)
        u = (pl or {}).get("usage") or {}
        row = {"act": a["id"], "kind": a["kind"], "repeat": r, "model": (pl or {}).get("model"),
               "http_status": st, "latency_s": round(dt, 4), "input_tokens": u.get("input_tokens"),
               "labels": a["labels"], "answers": (pl or {}).get("answers") or {}}
        with lock:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            fh.flush()
            spent["usd"] += (u.get("input_tokens") or 0) * PRICE
        return row

    with ThreadPoolExecutor(max_workers=8) as ex:
        rows = list(ex.map(run, [(a, r) for a in acts for r in range(REPEATS)]))
    fh.close()
    score(acts, rows, spent)
    return 0


if __name__ == "__main__":
    sys.exit(main())
