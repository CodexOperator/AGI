#!/usr/bin/env python3
"""Arm B (Bonsai 2 27B PTQ1_0, no LoRA) IFEval response generator.

Same request shape as ifeval_gen.py reference, but:
  base_url default = fork at :8899
  model id = whatever /v1/models reports
  adds llama.cpp chat_template_kwargs {"enable_thinking": false}
  output armB_bonsai27b-ptq1.ifeval.responses.jsonl (in cwd)
Resumable & shardable: <input> [base_url] [shard] [nshards]
"""
import json, os, sys, time, urllib.request

SRC = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "http://[REDACTED]:8899"
SHARD = int(sys.argv[3]) if len(sys.argv) > 3 else 0
NSH = int(sys.argv[4]) if len(sys.argv) > 4 else 1
OUT = "armB_bonsai27b-ptq1.ifeval.responses.jsonl" + (f".shard{SHARD}" if NSH > 1 else "")
MODEL = json.load(urllib.request.urlopen(BASE + "/v1/models"))["data"][0]["id"]

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
                "max_tokens": 1280, "stream": False,
                "chat_template_kwargs": {"enable_thinking": False}}
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
