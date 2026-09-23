#!/usr/bin/env python3
"""KV-format round: does q8_0/q4_0 KV buy context at <=0.5/2 pct NLL on the served 9B?

T1 llama-perplexity (f16 twice, then q8_0, q4_0) -- quality.
T2 llama-server with the ROUTER'S OWN recorded args (--fit on, --parallel 1, --cache-reuse 8,
   --jinja) + -fa on -ctk T -ctv T, spare port -> the fitted n_ctx.
T3 llama-bench -p 0 -n 64 -d 16384 -> tg tok/s (recorded, not a verdict input).
Caller stops the router first and restores it after; this script never touches it.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")):
    ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing"))
import paths

IMG = "ghcr.io/ggml-org/llama.cpp:full-cuda"
SCRATCH = "/data/ml/scratch/osc02"  # proposed box.ml_scratch_dir
GGUF = SCRATCH + "/Qwen3.5-9B-Q4_K_M.gguf"
TYPES = ["f16", "q8_0", "q4_0"]
PORTS = {"f16": 18081, "q8_0": 18082, "q4_0": 18083}
OUT = paths.get_local("kv_format_out_dir")
LOG = os.path.join(OUT, "logs")
# the 9B's exact router args, /v1/models status.args, --port replaced per T2
SRV = ["--cache-reuse", "8", "--host", "127.0.0.1", "--jinja", "--alias", "Qwen3.5-9B-Q4_K_M",
       "--fit", "on", "--model", "/work/Qwen3.5-9B-Q4_K_M.gguf", "--parallel", "1"]
MODEL = ["-m", "/work/Qwen3.5-9B-Q4_K_M.gguf"]


def run(entry, args, name, timeout=2400):
    os.makedirs(LOG, exist_ok=True)
    cmd = ["docker", "run", "--rm", "--gpus", "all", "-v", SCRATCH + ":/work",
           "--entrypoint", "/app/" + entry, IMG] + args
    t0, p = time.time(), None
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    out = p.stdout + p.stderr
    open(os.path.join(LOG, name + ".log"), "w").write(out)
    print("[%s] exit=%d secs=%.0f" % (name, p.returncode, time.time() - t0), flush=True)
    return p.returncode, out


def ram():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) // 1024
    return -1


def ppl(tag, name):
    rc, out = run("llama-perplexity", MODEL + ["-f", "/work/wikitext-2-raw/wiki.test.raw",
                 "-c", "512", "--chunks", "40", "-ngl", "99", "-fa", "on", "-ctk", tag,
                 "-ctv", tag, "--seed", "42", "-t", "8", "--no-warmup"], name)
    m = re.findall(r"PPL\s*=\s*([0-9.]+)", out)
    return {"rc": rc, "ppl": float(m[-1]) if m else None}


def fit(tag):
    """n_ctx the server FITS on the free card with the router's own args (--fit on).

    The router's args bind --host 127.0.0.1, so a -p mapping cannot reach /props
    (docker DNAT targets the container IP, not its loopback); the load log's
    `n_ctx_slot = N`, printed once the server is listening, is the fitted figure.
    """
    name, port = "kvfit-" + tag, PORTS[tag]
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    subprocess.Popen(["docker", "run", "-d", "--rm", "--name", name, "--gpus", "all",
                      "-v", SCRATCH + ":/work", "-p", "127.0.0.1:%d:%d" % (port, port),
                      "--entrypoint", "/app/llama-server", IMG] +
                     SRV[:4] + ["--port", str(port)] + SRV[4:] +
                     ["-fa", "on", "-ctk", tag, "-ctv", tag], stdout=subprocess.DEVNULL)
    n_ctx, txt = None, ""
    for _ in range(120):
        time.sleep(3)
        log = subprocess.run(["docker", "logs", name], capture_output=True, text=True)
        txt = log.stdout + log.stderr
        m = re.search(r"n_ctx_slot = (\d+)", txt)
        if m and "listening on" in txt:
            n_ctx = int(m.group(1))
            break
    subprocess.run(["docker", "stop", name], capture_output=True)
    os.makedirs(LOG, exist_ok=True)
    open(os.path.join(LOG, "fit_" + tag + ".log"), "w").write(txt)
    return {"n_ctx": n_ctx, "ram_mb": ram(), "rc": 0 if n_ctx else 1}


def bench(tag):
    args = MODEL + ["-ngl", "99", "-fa", "1", "-ctk", tag, "-ctv", tag,
                    "-p", "0", "-n", "64", "-d", "16384", "-r", "2"]
    run("llama-bench", args, "bench_warm_" + tag)
    rc, out = run("llama-bench", args, "bench_" + tag)
    tg = None
    for line in out.splitlines():
        if "tg64" in line and "d16384" in line:
            tg = float(line.split("|")[-2].strip().split()[0])
    return {"rc": rc, "tg_tok_s": tg}


res = {"ram_mb_start": ram(),
       "model_sha256": subprocess.run(["sha256sum", GGUF], capture_output=True, text=True).stdout.split()[0],
       "router_args_recorded": SRV, "types": {}}
for tag in TYPES:
    r = {"ppl": ppl(tag, "ppl_" + tag)}
    if tag == "f16":
        r["ppl_run2"] = ppl(tag, "ppl_f16_2")
    r["fit"] = fit(tag)
    r["bench"] = bench(tag)
    r["ram_mb_end"] = ram()
    res["types"][tag] = r
    print(json.dumps({tag: r}), flush=True)
os.makedirs(OUT, exist_ok=True)
json.dump(res, open(os.path.join(OUT, "kv_format.json"), "w"), indent=1)
print("WROTE", os.path.join(OUT, "kv_format.json"))
