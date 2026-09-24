#!/usr/bin/env python3
"""OSC.11 micro-batch prefill round on the served 9B: T1 the (KV type x -ub) matrix on ~30k-token
prompts, T2 the paired gain per KV type vs its -ub 512 arm and each KV type's cost vs f16, T3 the
persistent-JIT-cache proof. A fresh llama-server per arm on a spare port, the router's recorded args
verbatim plus -fa on / -ctk / -ctv / -ub / -b; a persistent /root/.nv/ComputeCache is mounted so a
fresh container pays the sm_75 PTX JIT once, not per arm. The CALLER stops llama-server first and
restores it after; this script never touches it.
Stage: `python3 ub_prefill_round.py t1|t2|t3`; every path via paths.get_local (rule 13)."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")): ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing"))
import paths
IMG = "ghcr.io/ggml-org/llama.cpp:server-cuda"; SC = paths.get("osc02_scratch_dir"); CACHE = paths.get("cuda_jit_cache_dir")
M = "/work/Qwen3.5-9B-Q4_K_M.gguf"
OUT = paths.get_local("serving_sweep_ub_out_dir"); LOG = OUT + "/logs"
ARGS = ["--cache-reuse", "8", "--host", "0.0.0.0", "--jinja", "--alias", "Qwen3.5-9B-Q4_K_M", "--fit", "on",
        "--model", M, "--parallel", "1"]
RAW = open(SC + "/wikitext-2-raw/wiki.test.raw", "rb").read()
os.makedirs(LOG, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
SLICES = {"s1": (10000, 132000), "s2": (400000, 132000), "s3": (800000, 132000)}
KVS = ["f16", "q8_0", "q4_0"]; UBS = [512, 1024, 2048]; T975_3 = 4.302653  # t_0.975, df=2


def post(port, text, k):
    p = os.path.join(OUT, "req_%s.json" % k)
    json.dump({"model": "Qwen3.5-9B-Q4_K_M", "messages": [{"role": "user", "content": text}], "max_tokens": 8,
               "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}, open(p, "w"))
    r = subprocess.run(["curl", "-s", "--max-time", "1800", "-X", "POST", "http://127.0.0.1:%d/v1/chat/completions" % port,
                        "-H", "Content-Type: application/json", "-d", "@" + p], capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except Exception: return {"_parse_error": r.stdout[:400]}


def up(port, name, tmo=420):
    t0 = time.time()
    while time.time() - t0 < tmo:
        if subprocess.run(["curl", "-sf", "--max-time", "3", "http://127.0.0.1:%d/health" % port], capture_output=True).returncode == 0:
            return round(time.time() - t0, 1)
        if subprocess.run(["docker", "inspect", "-f", "{{.State.Running}}", name], capture_output=True, text=True).stdout.strip() != "true":
            return None  # OOM-killed or exited: do not burn the whole timeout
        time.sleep(2)
    return None


def arm(kv, ub, port):
    name = "ub_%s_%d" % (kv, ub)
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    subprocess.run(["docker", "run", "--rm", "-d", "--name", name, "--gpus", "all", "-v", SC + ":/work", "-v", OUT + ":/out",
                    "-v", CACHE + ":/root/.nv/ComputeCache", "-p", "127.0.0.1:%d:%d" % (port, port),
                    "--entrypoint", "/app/llama-server", IMG] + ARGS
                   + ["-fa", "on", "-ctk", kv, "-ctv", kv, "-ub", str(ub), "-b", str(max(2048, ub)),
                      "--port", str(port), "-lv", "3", "--log-file", "/out/logs/%s.log" % name], capture_output=True, text=True)
    load = up(port, name)
    try: n_ctx = json.loads(subprocess.run(["curl", "-s", "--max-time", "5", "http://127.0.0.1:%d/slots" % port],
                                           capture_output=True, text=True).stdout)[0].get("n_ctx")
    except Exception: n_ctx = None
    warm = post(port, "hi", "%s_w" % name).get("timings", {}) or {}
    rows = []
    for k, (off, n) in (SLICES.items() if load is not None else {}):
        tm = post(port, RAW[off:off + n].decode("utf-8", "replace"), "%s_%s" % (name, k)).get("timings", {}) or {}
        rows.append({x: tm.get(x) for x in ("prompt_n", "prompt_ms", "prompt_per_second", "predicted_n", "cache_n")}
                    | {"slice": k, "off": off, "bytes": n})
        if rows[-1]["prompt_n"]: rows[-1]["ms_per_token"] = round(rows[-1]["prompt_ms"] / rows[-1]["prompt_n"], 3)
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    out = {"kv": kv, "ub": ub, "b": max(2048, ub), "port": port, "load_s": load, "n_ctx": n_ctx,
           "warmup": {x: warm.get(x) for x in ("prompt_n", "prompt_ms", "prompt_per_second")}, "rows": rows}
    json.dump(out, open(LOG + "/%s.json" % name, "w"), indent=1)
    print(name, json.dumps(out), flush=True); return out


def load(): return json.load(open(OUT + "/ub.json")) if os.path.exists(OUT + "/ub.json") else {}


def save(stage, res):
    d = load(); d[stage] = res; json.dump(d, open(OUT + "/ub.json", "w"), indent=1); print("WROTE", OUT + "/ub.json", stage, flush=True)


def t1(only=None):
    res = {}; port = 18100
    for kv in KVS:
        for ub in UBS:
            key = "%s_%d" % (kv, ub)
            if only is None or key in only: res[key] = arm(kv, ub, port)
            port += 1
    old = load().get("t1", {}).get("arms", {}); old.update(res)
    save("t1", {"slices": SLICES, "arms": old})


def ci(g, n=3):
    m = sum(g) / n; v = sum((x - m) ** 2 for x in g) / (n - 1)
    hw = T975_3 * (v / n) ** .5
    return {"mean": round(m, 4), "lo": round(m - hw, 4), "hi": round(m + hw, 4), "n": n}


def t2():
    a = load()["t1"]["arms"]; base = {}
    for kv in KVS:
        base[kv] = [r["prompt_per_second"] for r in a["%s_512" % kv]["rows"]]
    out = {}
    for kv in KVS:
        for ub in UBS:
            if ub == 512: continue
            tps = [r["prompt_per_second"] for r in a["%s_%d" % (kv, ub)]["rows"]]
            g = [tps[i] / base[kv][i] - 1 for i in range(3)]
            ci_ = ci(g)
            out["%s_%d" % (kv, ub)] = {"gain_ci": ci_, "clears_zero": ci_["lo"] > 0, "ge_10pct": ci_["lo"] >= 0.10,
                                       "mean_tps": round(sum(tps) / 3, 1), "n_ctx": a["%s_%d" % (kv, ub)]["n_ctx"],
                                       "ms_per_token": round(sum(r["prompt_ms"] / r["prompt_n"] for r in a["%s_%d" % (kv, ub)]["rows"]) / 3, 3)}
    f16b = base["f16"]
    for kv in KVS:
        if kv == "f16": continue
        tps = base[kv]
        out["%s_512_vs_f16" % kv] = {"cost_ci": ci([f16b[i] / tps[i] - 1 for i in range(3)])}
    save("t2", out)


def t3():
    a = load()["t1"]["arms"]
    w = {k: v["warmup"] for k, v in sorted(a.items(), key=lambda x: x[1]["port"])}
    save("t3", {"first_arm": next(iter(w)), "warmups": w})


if __name__ == "__main__":
    st = sys.argv[1]
    if st == "t1": t1(set(sys.argv[2].split(",")) if len(sys.argv) > 2 else None)
    else: {"t2": t2, "t3": t3}[st]()
