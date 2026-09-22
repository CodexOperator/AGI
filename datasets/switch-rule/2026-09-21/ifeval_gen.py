#!/usr/bin/env python3
"""Generate IFEval reference responses, one per prompt in input_data.jsonl order.

Resumable and shardable: run N workers with disjoint (shard, nshards) args; each
appends to its own .shard<k> file and skips prompts already present, so a restart
never re-pays. Merge the shards into the final ordered file afterward.
Calls proxy.py so the request shape and thinking-off expression match HumanEval.
Usage: ifeval_gen.py <input_data.jsonl> [base_url] [shard] [nshards]
"""
import json, os, sys, time, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://127.0.0.1:8787"
SHARD = int(sys.argv[3]) if len(sys.argv) > 3 else 0
NSH = int(sys.argv[4]) if len(sys.argv) > 4 else 1
OUT = os.path.join(D, "ref_ifeval_deepseek-v4.1-flash.responses.jsonl"
                   + (f".shard{SHARD}" if NSH > 1 else ""))
MODEL = "deepseek/deepseek-v4.1-flash"

prompts = [json.loads(l)["prompt"] for l in open(SRC) if l.strip()]
mine = [p for i, p in enumerate(prompts) if i % NSH == SHARD]
got = {}
if os.path.exists(OUT):
    for line in open(OUT):
        if line.strip():
            row = json.loads(line)
            got[row["prompt"]] = row["response"]

with open(OUT, "a") as f:
    for p in mine:
        if p in got:
            continue
        body = {"model": MODEL, "messages": [{"role": "user", "content": p}],
                "temperature": 0.0, "top_p": 1.0, "seed": 1234,
                "max_tokens": 1280, "stream": False}
        req = urllib.request.Request(BASE + "/v1/chat/completions",
                                     data=json.dumps(body).encode(),
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=900) as r:
                resp = json.load(r)
            got[p] = resp["choices"][0]["message"]["content"] or ""
        except Exception as e:
            print("ERR", p[:50], repr(e), flush=True)
            time.sleep(3)
            continue
        f.write(json.dumps({"prompt": p, "response": got[p]}) + "\n")
        f.flush()
        print(f"shard{SHARD} {len(got)}/{len(mine)}", flush=True)
print(f"shard{SHARD} done {len(got)}/{len(mine)}", flush=True)