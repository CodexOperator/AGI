#!/usr/bin/env python3
"""JEV.01 ECHO arm -- hypothesis:lm-jev-verdict-agreement-is-leak-echo.

Same corpus, prompts, model, seed and repeats as acts_replay.py. ONE new
variable: before the call, every verdict/status token in the node BODY is
replaced by a fixed neutral placeholder. Separate cache and row files, or the
unscrubbed json_cache would satisfy every lookup (its key omits the state).

The corpus is PINNED to the act ids already in acts_replay.jsonl, because the
seeded draw in acts_replay.py runs over a live directory and re-sampling now
yields a different 200 experiments (only 211/370 acts overlap with JEV.01).
Both arms are re-run on that pinned corpus so before and after are matched.

  python3 acts_replay_scrub.py --dry   # corpus + leak counts, no network
  python3 acts_replay_scrub.py         # 2 x 1110 new calls, then score to .md
"""
import hashlib, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
import acts_replay as J

HERE = os.path.dirname(os.path.abspath(__file__))
SCRUB_CACHE, SCRUB_ROWS, MD = (os.path.join(HERE, n) for n in ("json_cache_scrub", "acts_replay_scrub.jsonl", "acts_replay_scrub.md"))
BEFORE_CACHE, BEFORE_ROWS, OLD_ROWS = (os.path.join(HERE, n) for n in ("json_cache_before", "acts_replay_before.jsonl", "acts_replay.jsonl"))
PLACEHOLDER = "[SCRUBBED]"
PAT = re.compile("inconclusive_lean_proved|inconclusive_lean_disproved|proved|disproved|pending|accept|demote", re.I)


def scrub(state):
    out = PAT.sub(PLACEHOLDER, state)
    return out, len(PAT.findall(state)), len(PAT.findall(out))


def _scan(kind):
    d = os.path.join(J.NODES, kind)
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        t = open(os.path.join(d, fn), encoding="utf-8", errors="replace").read()
        m = re.match(r"---[ \t]*\n(.*?)\n---[ \t]*\n", t, re.S)
        fm, body = (m.group(1), t[m.end():]) if m else ("", t)
        yield (J.field(fm, "id") or kind + ":" + fn[:-3]), kind, fm, body


def pinned_corpus():
    ids, seen = [], set()
    for line in open(OLD_ROWS, encoding="utf-8"):
        r = json.loads(line)
        if r["act"] not in seen:
            seen.add(r["act"]); ids.append(r["act"])
    found = {}
    for kind in ("verdict", "experiment"):
        for aid, k, fm, body in _scan(kind):
            found[aid] = (k, fm, body)
    out, gone = [], []
    for aid in ids:
        if aid not in found:
            gone.append(aid)
            continue
        kind, fm, body = found[aid]
        lab = {}
        v = J.norm(J.field(fm, "verdict"))
        if v:
            lab["q1"] = v
        lab["q2"] = "demote" if J.field(fm, "demoted_from") else "accept"
        pl, lc = J.field(fm, "production_lines"), J.field(fm, "line_ceiling")
        if pl.isdigit() and lc.isdigit():
            lab["q4"] = "big" if int(pl) > int(lc) else "small"
        out.append({"id": aid, "kind": kind, "state": body[:128000], "labels": lab})
    if gone:
        sys.stderr.write("missing node files for %d act ids: %s\n" % (len(gone), gone[:5]))
    return out


def run_arm(acts, do_scrub, cache, rows_path):
    key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_KEY")
    fh = open(rows_path, "w", encoding="utf-8")
    spent, lock = {"usd": 0.0}, __import__("threading").Lock()
    states, leaks = {}, {}
    for a in acts:
        s, leaks[a["id"]], after = scrub(a["state"]) if do_scrub else (a["state"], 0, 0)
        states[a["id"]] = s

    def run(job):
        a, r = job
        ck = hashlib.sha256(("%s|%d|%s|%s" % (a["id"], r, J.MODEL, PLACEHOLDER if do_scrub else "plain")).encode()).hexdigest()[:24]
        cp = os.path.join(cache, ck + ".json")
        if os.path.exists(cp):
            d = json.load(open(cp)); st, pl = d["http_status"], d["payload"]
        elif spent["usd"] >= J.CAP:
            st, pl = 0, {"blocked": "budget_cap"}
        else:
            st, pl, _ = J.ask(key, states[a["id"]])
            if st != 200:
                st, pl, _ = J.ask(key, states[a["id"]])
            json.dump({"act": a["id"], "repeat": r, "model": J.MODEL, "arm": PLACEHOLDER if do_scrub else "plain",
                       "http_status": st, "payload": pl}, open(cp, "w", encoding="utf-8"), ensure_ascii=False)
        u = (pl or {}).get("usage") or {}
        row = {"act": a["id"], "kind": a["kind"], "repeat": r, "arm": PLACEHOLDER if do_scrub else "plain",
               "model": (pl or {}).get("model"), "http_status": st, "input_tokens": u.get("input_tokens"),
               "labels": a["labels"], "leak_before": leaks[a["id"]],
               "leak_after": len(PAT.findall(states[a["id"]])), "answers": (pl or {}).get("answers") or {}}
        with lock:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n"); fh.flush()
            spent["usd"] += (u.get("input_tokens") or 0) * J.PRICE
        return row

    with ThreadPoolExecutor(max_workers=8) as ex:
        rws = list(ex.map(run, [(a, r) for a in acts for r in range(J.REPEATS)]))
    fh.close()
    return rws, spent, leaks


def group(rws):
    by = {}
    for r in rws:
        by.setdefault(r["act"], []).append(r)
    return by


def majority(rs, q):
    ps = [p for p in (J.pick(r, q)[0] for r in rs) if p]
    return max(set(ps), key=ps.count) if ps else None


def agree(by, q):
    n = ok = 0
    labs = []
    for rs in by.values():
        lab = rs[0]["labels"].get(q)
        if lab is None:
            continue
        n += 1; labs.append(lab)
        ok += majority(rs, q) == lab
    base = max(labs.count(x) for x in set(labs)) / n if n else 0
    cls = sorted(set(labs))
    return n, ok / n if n else 0, base, cls


def main():
    dry = "--dry" in sys.argv
    acts = pinned_corpus()
    leaks = {a["id"]: scrub(a["state"])[1] for a in acts}
    print("acts=%d verdict=%d experiment=%d leak_before=%d leaked_acts=%.3f residual_after=%d" % (
        len(acts), sum(a["kind"] == "verdict" for a in acts), sum(a["kind"] == "experiment" for a in acts),
        sum(leaks.values()), sum(1 for v in leaks.values() if v) / len(acts), sum(scrub(a["state"])[2] for a in acts)))
    if dry:
        return 0
    key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("TYPESAFE_KEY")
    if not key:
        sys.stderr.write("blocked:no_key -- 0 network calls\n"); return 2
    for d in (SCRUB_CACHE, BEFORE_CACHE):
        os.makedirs(d, exist_ok=True)
    brows, bspent, _ = run_arm(acts, False, BEFORE_CACHE, BEFORE_ROWS)
    srows, sspent, ls = run_arm(acts, True, SCRUB_CACHE, SCRUB_ROWS)
    B, S = group(brows), group(srows)
    lines = ["# acts_replay_scrub -- ECHO arm", "",
             "MODEL=%s; SEED=%d; REPEATS=%d; state = node BODY only; scrub replaces every proved|disproved|inconclusive_lean_*|pending|accept|demote token with %s." % (J.MODEL, J.SEED, J.REPEATS, PLACEHOLDER),
             "Corpus PINNED to the %d act ids in acts_replay.jsonl (JEV.01 re-samples a different 200 experiments now; only 211/370 overlap)." % len(acts),
             "Calls 200: before %d / after %d. Spend: before $%.6f + after $%.6f = $%.6f (cap $%.2f)." % (
                 sum(1 for r in brows if r["http_status"] == 200), sum(1 for r in srows if r["http_status"] == 200), bspent["usd"], sspent["usd"], bspent["usd"] + sspent["usd"], J.CAP),
             "", "| q | n | agree BEFORE | agree AFTER | base | chance |", "|---|---|---|---|---|---|"]
    res = {}
    for q in ("q1", "q2"):
        n1, b, base, cls = agree(B, q)
        n2, a, _, _ = agree(S, q)
        chance = 1.0 / len(cls) if q == "q1" else ""
        res[q] = (b, a)
        lines.append("| %s | %d | %.3f | %.3f | %.3f | %s |" % (q, n1, b, a, base, ("%.3f" % chance) if chance != "" else "na"))
    classes = agree(S, "q1")[3]
    chance = 1.0 / len(classes)
    lb = sum(ls.values())
    la = sum(r["leak_after"] for r in srows)
    lines += ["", "- q1 distinct verdict classes present: %d -> chance = 1/%d = %.3f; claim bar chance+0.10 = %.3f" % (len(classes), len(classes), chance, chance + 0.10),
              "- q1 delta = %+.3f; falsifier 1 (ECHO wrong) trips if q1_after >= 0.60" % (res["q1"][1] - res["q1"][0]),
              "- q2 delta = %+.3f; falsifier 3 trips if |delta| > 0.10" % (res["q2"][1] - res["q2"][0]),
              "- leak tokens before (act total): %d; leaked acts fraction %.3f; after (row total): %d; residual act ids: %s" % (lb, sum(1 for v in ls.values() if v) / len(ls), la, [r["act"] for r in srows if r["leak_after"]][:5]),
              "- JEV.01 historical reference (old re-sampled corpus): q1 0.743 base 0.507, q2 0.492 base 0.776"]
    open(MD, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
