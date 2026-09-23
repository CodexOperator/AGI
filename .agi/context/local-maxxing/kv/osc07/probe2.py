#!/usr/bin/env python3
"""OSC.07 probe 2: (a) clean re-measure of the --fit capacity reps (the first run's 86,528
looks contaminated by a concurrent manual llama-server); (b) FA on/off A/B on the split.
Session scratch only -- not production. Reuses kv_split_round.__main__-guarded helpers."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # kv/, resolved from this file
import kv_split_round as K

res = {"fits": [], "fa_ab": {}}
for i, (ctk, ctv) in enumerate([("q8_0", "q4_0"), ("f16", "f16"), ("q8_0", "q4_0"), ("f16", "f16"),
                                ("q8_0", "q4_0")]):
    r = K.fit(ctk, ctv, "clean%d_%s_%s" % (i, ctk, ctv), 18087 + i)
    row = {"rep": i, "ctk": ctk, "ctv": ctv, "n_ctx": r["n_ctx"], "ratio": r["n_ctx"] / 49664.0}
    res["fits"].append(row)
    print("FIT " + json.dumps(row), flush=True)

for tag, (ctk, ctv), fa in [("split_fa1", ("q8_0", "q4_0"), 1), ("split_fa0", ("q8_0", "q4_0"), 0),
                            ("f16_fa0", ("f16", "f16"), 0)]:
    REPS = 3  # this probe runs -r 3; parse() records it
    a = ["-m", K.M, "-ngl", "99", "-fa", str(fa), "-ctk", ctk, "-ctv", ctv, "-p", "0", "-n", "64",
         "-d", "16384"]
    K.run("llama-bench", a + ["-r", "1"], tag + "_warm")
    res["fa_ab"][tag] = K.S.parse(K.run("llama-bench", a + ["-r", str(REPS)], tag), REPS)
    print("BENCH " + tag + " " + json.dumps(res["fa_ab"][tag]), flush=True)

json.dump(res, open(K.OUT + "/probe2.json", "w"), indent=1)
print("WROTE", K.OUT + "/probe2.json")
