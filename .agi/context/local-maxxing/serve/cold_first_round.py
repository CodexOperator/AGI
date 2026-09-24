#!/usr/bin/env python3
"""OSC.09 cold-first-request round on the served 9B: T1 cold vs warm (3 trials), T2 tiny warm-up (does W make A
warm), T3 size sweep (256/2k/8k), T4 -lv 5 first-vs-second request logs.
Fresh llama-server per trial on a spare port, the router's recorded args (verbatim but for --port, --host 0.0.0.0
and the in-container model path; no -fa/-ctk/-ctv added). The CALLER stops llama-server first and restores it after; this script never touches it.
Stage: `python3 cold_first_round.py t1|t2|t3|t4`; every path via paths.get_local (rule 13)."""
import json, os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")): ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing"))
import paths
IMG = "ghcr.io/ggml-org/llama.cpp:full-cuda"; IMG2 = "ghcr.io/ggml-org/llama.cpp:server-cuda"; SC = paths.get("osc02_scratch_dir"); M = "/work/Qwen3.5-9B-Q4_K_M.gguf"
OUT = paths.get_local("serving_sweep_cold_out_dir"); LOG = OUT + "/logs"; WIKI = SC + "/wikitext-2-raw/wiki.test.raw"
ARGS = ["--cache-reuse", "8", "--host", "0.0.0.0", "--jinja", "--alias", "Qwen3.5-9B-Q4_K_M", "--fit", "on", "--model", M, "--parallel", "1"]
RAW = open(WIKI, "rb").read()
os.makedirs(LOG, exist_ok=True)


def sl(off, n):  # a wikitext-2 slice, byte offsets recorded in cold.json
    return {"text": RAW[off:off + n].decode("utf-8", "replace"), "off": off, "bytes": n}


def post(port, text, k):
    p = os.path.join(OUT, "cold_req_%s.json" % k)
    json.dump({"model": "Qwen3.5-9B-Q4_K_M", "messages": [{"role": "user", "content": text}], "max_tokens": 8,
               "temperature": 0, "chat_template_kwargs": {"enable_thinking": False}}, open(p, "w"))
    r = subprocess.run(["curl", "-s", "--max-time", "900", "-X", "POST", "http://127.0.0.1:%d/v1/chat/completions" % port,
                        "-H", "Content-Type: application/json", "-d", "@" + p], capture_output=True, text=True)
    try: return json.loads(r.stdout)
    except Exception: return {"_parse_error": r.stdout[:400]}


def up(port, tmo=600):
    t0 = time.time()
    while time.time() - t0 < tmo:
        if subprocess.run(["curl", "-sf", "--max-time", "3", "http://127.0.0.1:%d/health" % port], capture_output=True).returncode == 0:
            return round(time.time() - t0, 1)
        time.sleep(1)
    return None


def trial(name, port, slices, lv=1, img=IMG):
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    subprocess.run(["docker", "run", "--rm", "-d", "--name", name, "--gpus", "all", "-v", SC + ":/work", "-v", OUT + ":/out",
                    "-p", "127.0.0.1:%d:%d" % (port, port), "--entrypoint", "/app/llama-server", img]
                   + ARGS + ["--port", str(port), "-lv", str(lv), "--log-file", "/out/%s.log" % name], capture_output=True, text=True)
    load = up(port); rows = []
    for i, s in enumerate(slices):
        tm = post(port, s["text"], "%s_%d" % (name, i)).get("timings", {}) or {}
        rows.append({k: tm.get(k) for k in ("prompt_n", "prompt_ms", "prompt_per_second", "predicted_n", "cache_n")}
                    | {"size_off": s["off"], "size_bytes": s["bytes"]})
        if rows[-1]["prompt_n"]: rows[-1]["ms_per_token"] = round(rows[-1]["prompt_ms"] / rows[-1]["prompt_n"], 3)
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    out = {"name": name, "port": port, "load_s": load, "lv": lv, "img": img, "rows": rows}
    json.dump(out, open(LOG + "/%s.json" % name, "w"), indent=1)
    print(name, json.dumps(out), flush=True); return out


S = {"a": sl(10000, 9000), "b": sl(40000, 9000), "w": {"text": "hi", "off": None, "bytes": 2},
     "s256": sl(100000, 1100), "s8k": sl(200000, 34000)}


def save(stage, res):
    old = json.load(open(OUT + "/cold.json")) if os.path.exists(OUT + "/cold.json") else {}
    old[stage] = res; json.dump(old, open(OUT + "/cold.json", "w"), indent=1); print("WROTE", OUT + "/cold.json", stage, flush=True)


if __name__ == "__main__":
    st = sys.argv[1]
    if st == "t1": save("t1", {"slices": {k: {"off": S[k]["off"], "bytes": S[k]["bytes"]} for k in ("a", "b")},
                               "trials": [trial("t1r%d" % i, 18081 + i, [S["a"], S["b"]]) for i in range(3)]})
    elif st == "t2": save("t2", {"slices": {k: {"off": S[k]["off"], "bytes": S[k]["bytes"]} for k in ("w", "a")},
                                 "trials": [trial("t2r%d" % i, 18084 + i, [S["w"], S["a"]]) for i in range(3)]})
    elif st == "t3": save("t3", {"trials": [trial("t3_" + k, 18087 + i, [S[k]]) for i, k in enumerate(("s256", "a", "s8k"))]})
    elif st == "t4": save("t4", trial("t4", 18090, [S["a"], S["b"]], lv=5))
    elif st == "tf": save("tf", trial("tf0", 18091, [S["w"], S["a"]], img=IMG2))