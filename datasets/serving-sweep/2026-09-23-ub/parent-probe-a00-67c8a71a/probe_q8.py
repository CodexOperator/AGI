#!/usr/bin/env python3
"""PARENT negative probe for OSC.11 claim conjunct 1: re-measure the q8_0 -ub 512 baseline and the
paired q8_0 -ub 1024 arm on the now-quiet box, same slices, same image/args. If the -ub 512 baseline
rises to the ~1200 tok/s of its siblings the "+27 pct gain" is an environment artifact of the
contended original run and the claim's main conjunct fails. Reuses the kid's driver unmodified,
with OUT/LOG redirected into this scratch dir so the kid's ub.json is never touched."""
import json, os, sys
ROOT = "/data/work/agi/.agi/worktrees/a00-67c8a71a"
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing/serve"))
import ub_prefill_round as M
PROBE = os.path.join(ROOT, ".agi/sessions/iter-OSC.11/a00-67c8a71a/probe")
os.makedirs(PROBE, exist_ok=True)
M.OUT = PROBE; M.LOG = PROBE
res = {}
for kv, ub, port in [("q8_0", 512, 18130), ("q8_0", 1024, 18131)]:
    key = "%s_%d" % (kv, ub)
    print("PROBE ARM", key, flush=True)
    res[key] = M.arm(kv, ub, port)
json.dump(res, open(os.path.join(PROBE, "probe_q8.json"), "w"), indent=1)
print("PROBE DONE", flush=True)
