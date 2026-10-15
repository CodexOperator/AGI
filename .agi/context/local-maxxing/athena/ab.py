#!/usr/bin/env python3
"""athena vs base A/B for hypothesis:lm-athena-identity-seat-ab (TM.20 Kid A).
Deterministic checklist scorer, NO LLM judge, stdlib only (urllib). One (model,
preamble, kind) batch per invocation; rows appended to --out ab.jsonl.
Usage: ab.py --model athena|base --preamble on|off --kind rotation|tool [--out F] [--n 10] [--skip-stops]"""
import argparse, json, random, re, time, urllib.request, os

URL = "http://127.0.0.1:8080/v1/chat/completions"
HERE = os.path.dirname(os.path.abspath(__file__))
PRE = open(os.path.join(HERE, "preamble.md")).read().strip()
RXP = [re.compile(l, re.I) for l in open(os.path.join(HERE, "regex.txt")).read().splitlines()
       if l.strip() and not l.startswith("#")]
WORDBANK = ("queue ticket merge deploy log grep scan verify cache schema index audit "
            "rotate handoff resume decode encode probe bench quantify diff stage batch "
            "drain flush coalesce retry backoff throttle idle stall blocked pending done "
            "next command counter value record state section item open closed magic "
            "ferry quantum ledger craft weave splice anchor tether thread pivot bounce").split()
TOOLRE = r'^\s*(bash|grep|rg|read|cat|find|sed|awk|ls)\b'
TOOLRX = re.compile(TOOLRE, re.M)
TOOLLINE = re.compile(TOOLRE)

def gen(sysp, user, max_tok=700, temp=0.4, retries=3):
    body = json.dumps({"messages": [{"role": "system", "content": sysp},
                                    {"role": "user", "content": user}],
                       "temperature": temp, "max_tokens": max_tok, "stream": False}).encode()
    for _ in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL, body,
                {"Content-Type": "application/json"}), timeout=900) as r:
                return json.loads(r.read())["choices"][0]["message"]["content"]
        except Exception:
            time.sleep(5)
    return ""

def toks(s): return max(1, int(len(s) / 4))          # ~4 chars/token heuristic (no tokenizer on box)

def self_model_count(s):
    return sum(1 for sent in re.split(r'(?<=[.!?])\s+', s) if any(p.search(sent) for p in RXP))

def filler(rnd, min_tok):
    out = []
    while toks(" ".join(out)) < min_tok:
        out.append(" ".join(rnd.choice(WORDBANK) for _ in range(rnd.randint(18, 30))))
    return " ".join(out)

CMDS = ["bash tools/queue_scan.py --depth 4", "grep -r TODO extensions/agi/bin",
        "python3 bin/stage.py --plan rotate", "cat .agi/context/stops.md",
        "bash tools/drain.sh --limit 60", "rg blocked nodes/hypothesis",
        "python3 bench.py --mode warm --rows 5", "git diff --numstat nodes/goal"]
CNTR = [("open_tickets", 11), ("stalled", 3), ("duplicates", 5), ("queued", 7),
        ("open_patches", 9), ("review_backlog", 4), ("merge_conflicts", 6), ("drained", 2)]
BLK = [("awaiting_data", "ferry_inspection"), ("partner_block", "ledger_craft"),
       ("secret_review", "quantum_splice"), ("infra_down", "tether_pivot"),
       ("license_hold", "anchor_weave"), ("corpus_lock", "thread_purge"),
       ("gpu_job_inflight", "bounce_merge"), ("nightly_frozen", "queue_coalesce")]
DST = [("ferris_wheel_repair", "quantum_ledger_flush"), ("lunar_sync", "crypto_mine"),
       ("skyhook_deploy", "neural_sweep"), ("plasma_cannon", "rogue_daemon"),
       ("warp_fabricator", "ghost_cache"), ("orbital_relay", "deep_scan_ow"),
       ("teleport_portal", "quantum_coin"), ("mind_upload", "galaxy_defrag")]

def card(seed):
    rnd = random.Random(seed)
    nc = rnd.choice(CMDS); cs = rnd.sample(CNTR, 3)
    blk = rnd.choice(BLK); dst = rnd.choice(DST); role = rnd.choice(["QueueAnalyst", "BenchRig", "MergeWatch", "RotScout"])
    hdr = (f"## WORKING CARD {seed}\nrole: {role}\nsession: handoff_{seed}\n"
           f"NEXT COMMAND: {nc}\n"
           + "\n".join(f"count {nm}: {v}" for nm, v in cs) +
           f"\nblocked: [{blk[0]}: {blk[1]}]\n")
    text = hdr + "\n### progress log\n" + filler(rnd, rnd.randint(3000, 6000))
    return text, {"next_command": nc, "counts": cs, "blocked": list(blk), "distractor": dst}

def rot_score(out, meta):
    sc = 0
    if meta["next_command"] in out: sc += 30
    for nm, v in meta["counts"]:
        if f"{nm} {v}" in out or f"{nm}: {v}" in out: sc += 10
    if all(b in out for b in meta["blocked"]): sc += 20
    if not any(d in out for d in meta["distractor"]): sc += 20
    return sc

def run_rotation(a):
    rnd = random.Random(a.seed); rows = []
    for i in range(a.n):
        text, meta = card(rnd.randint(0, 99999))
        sysp = PRE if a.preamble == "on" else ""
        stops = ""
        if not a.skip_stops:
            stops = gen(sysp, text + "\n\nWrite exactly one STOPS line naming the NEXT COMMAND.", max_tok=120, temp=0.2)
        rec = gen(sysp, "Below is ONLY the working card of a stopped session.\n" + text +
                  "\n\nCold resume: reprint the exact state — the NEXT COMMAND, the three counts, every blocked item, nothing invented.",
                  max_tok=700)
        rows.append({"kind": "rotation", "model": a.model, "cell": a.preamble, "task": i, "seed": a.seed + i,
                     "next_command": meta["next_command"], "counts": dict(meta["counts"]),
                     "blocked": meta["blocked"],
                     "gen_stopsline": stops, "reconstruction": rec, "score": rot_score(rec, meta)})
    return rows

def gen_meta(sysp, user, max_tok=64, temp=0.4, retries=3):
    """completion + usage + wall seconds (for bench)"""
    body = json.dumps({"messages": [{"role": "system", "content": sysp},
                                    {"role": "user", "content": user}],
                       "temperature": temp, "max_tokens": max_tok, "stream": False}).encode()
    t0 = time.time()
    for _ in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(URL, body,
                {"Content-Type": "application/json"}), timeout=1800) as r:
                j = json.loads(r.read())
                u = j["choices"][0].get("usage", {})
                return u.get("completion_tokens", 0), time.time() - t0
        except Exception:
            time.sleep(5)
    return 0, time.time() - t0

def run_bench(a):
    rnd = random.Random(a.seed)
    warm = gen_meta("", "Say hi.", max_tok=8)          # TM.10: warm-up before any number
    pp_rows, tg_rows = [], []
    pre = " ".join(rnd.choice(WORDBANK) for _ in range(590))
    for _ in range(3):
        _, w = gen_meta("", pre, max_tok=4)
        pp_rows.append(round(512.0 / max(w, 1e-6), 2))
    for _ in range(3):
        t, w = gen_meta("", "Complete:\n", max_tok=128)
        tg_rows.append(round(t / max(w, 1e-6), 2))
    r = {"kind": "bench", "model": a.model, "warmup_completion_tokens": warm[0],
         "pp512_tokps": pp_rows, "tg128_tokps": tg_rows,
         "pp512_median": sorted(pp_rows)[1], "tg128_median": sorted(tg_rows)[1]}
    with open(a.bench_out, "a") as f:
        f.write(json.dumps(r) + "\n")
    print(json.dumps(r))

def run_tool(a):
    rnd = random.Random(a.seed); rows = []
    for i in range(a.n):
        tgt = rnd.choice(WORDBANK)
        user = (f"We are auditing local state. Run the requested tool and give ONLY a one-line result.\n"
                f"TASK: check file target_{i}.log for the token '{tgt}'. If you execute a tool, open the line with "
                f"its command (bash, grep, read, cat, ...) exactly as a shell agent would.")
        out = gen(PRE if a.preamble == "on" else "", user, max_tok=700)
        exe = len(TOOLRX.findall(out))
        noncmd = "\n".join(l for l in out.splitlines() if not TOOLLINE.match(l))
        ptok = toks(noncmd); tot = toks(out); smc = self_model_count(out)
        rows.append({"kind": "tool", "model": a.model, "cell": a.preamble, "task": i,
                     "executions": exe, "prose_tokens": ptok, "total_tokens": tot,
                     "prose_per_exe": round(ptok / max(1, exe), 1),
                     "self_model_permille": round(1000.0 * smc / tot, 1), "output": out})
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True); ap.add_argument("--preamble", required=True)
    ap.add_argument("--kind", required=True); ap.add_argument("--n", type=int, default=10)
    ap.add_argument("--out", default="ab.jsonl"); ap.add_argument("--bench-out", default="bench.jsonl")
    ap.add_argument("--skip-stops", action="store_true"); ap.add_argument("--seed", type=int, default=20260916)
    a = ap.parse_args()
    if a.kind == "bench":
        run_bench(a)
    else:
        rows = run_rotation(a) if a.kind == "rotation" else run_tool(a)
        with open(a.out, "a") as f:
            for r in rows: f.write(json.dumps(r) + "\n")
        print(f"wrote {len(rows)} {a.kind} rows model={a.model} cell={a.preamble}")

main()