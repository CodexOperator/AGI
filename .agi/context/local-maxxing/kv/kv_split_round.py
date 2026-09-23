#!/usr/bin/env python3
"""KV-split round (OSC.07): is -ctk q8_0 -ctv q4_0 an L1 sibling of q4_0/q4_0 on the served 9B?

T1 placement: llama-server load log (-ctk q8_0 -ctv q4_0 -fa on) -- flash attention on CUDA or CPU?
T2 quality: llama-perplexity (f16 vs split, 40 x 512 wikitext-2 chunks). T3 capacity: the router's
own args with --fit on for the split, then the L1 stack (q4_0/q4_0) at --fit-target 512. T4 speed
(recorded): llama-bench tg64 @ d0/d16384, 5 reps, split vs q4_0/q4_0.
Caller stops the router and restores it; this script never touches it.
"""
import json, os, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")): ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing")); sys.path.insert(0, HERE)
import paths, kv_speed_round as S                     # __main__-guarded: reuse ram()/parse()
IMG = "ghcr.io/ggml-org/llama.cpp:full-cuda"
SCRATCH = "/data/ml/scratch/osc02"                    # proposed box.ml_scratch_dir
GGUF = SCRATCH + "/Qwen3.5-9B-Q4_K_M.gguf"; M = "/work/Qwen3.5-9B-Q4_K_M.gguf"
OUT = paths.get_local("kv_split_out_dir"); LOG = os.path.join(OUT, "logs")
SRV = ["--cache-reuse", "8", "--host", "127.0.0.1", "--jinja", "--alias", "Qwen3.5-9B-Q4_K_M",
       "--fit", "on", "--model", M, "--parallel", "1"]
FA = re.compile(r"flash|FA_QUANTS|CUDA|CPU|KV self|n_ctx_slot|not supported|fallback", re.I)


def run(entry, args, name, timeout=2400):
    os.makedirs(LOG, exist_ok=True); t0 = time.time()
    p = subprocess.run(["docker", "run", "--rm", "--gpus", "all", "-v", SCRATCH + ":/work",
                        "--entrypoint", "/app/" + entry, IMG] + args,
                       capture_output=True, text=True, timeout=timeout)
    out = p.stdout + p.stderr
    open(os.path.join(LOG, name + ".log"), "w").write(out)
    print("[%s] exit=%d secs=%.0f" % (name, p.returncode, time.time() - t0), flush=True)
    return out


def ppl(ctk, ctv, name):
    out = run("llama-perplexity", ["-m", M, "-f", "/work/wikitext-2-raw/wiki.test.raw", "-c",
              "512", "--chunks", "40", "-ngl", "99", "-fa", "on", "-ctk", ctk, "-ctv", ctv,
              "--seed", "42", "-t", "8", "--no-warmup"], name)
    m = re.findall(r"PPL\s*=\s*([0-9.]+)", out)
    return {"ppl": float(m[-1]) if m else None, "ram_mb": S.ram()}


def fit(ctk, ctv, name, port, fitt=None):
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)
    a = SRV + ["--port", str(port)] + (["--fit-target", str(fitt)] if fitt else [])
    subprocess.Popen(["docker", "run", "-d", "--rm", "--name", name, "--gpus", "all",
        "-v", SCRATCH + ":/work", "-p", "127.0.0.1:%d:%d" % (port, port),
        "--entrypoint", "/app/llama-server", IMG] + a + ["-fa", "on", "-ctk", ctk, "-ctv", ctv],
        stdout=subprocess.DEVNULL)
    txt, n = "", None
    for _ in range(140):
        time.sleep(3)
        lg = subprocess.run(["docker", "logs", name], capture_output=True, text=True)
        txt = lg.stdout + lg.stderr
        m = re.search(r"n_ctx_slot = (\d+)", txt)
        if m and "listening on" in txt: n = int(m.group(1)); break
    subprocess.run(["docker", "stop", name], capture_output=True)
    os.makedirs(LOG, exist_ok=True); open(os.path.join(LOG, name + ".log"), "w").write(txt)
    return {"n_ctx": n, "ram_mb": S.ram(), "fa_lines": [l for l in txt.splitlines() if FA.search(l)]}


def bench(ctk, ctv, name):
    a = ["-m", M, "-ngl", "99", "-fa", "1", "-ctk", ctk, "-ctv", ctv, "-p", "512", "-n", "64",
         "-d", "0,16384"]
    run("llama-bench", a + ["-r", "1"], name + "_warm")
    out = run("llama-bench", a + ["-r", str(S.REPS)], name)
    return {"rows": S.parse(out, S.REPS), "ram_mb": S.ram(), "loadavg": list(os.getloadavg())}


def main():
    res = {"image": IMG, "router_args": SRV, "ram_mb_start": S.ram(),
           "model_sha256": subprocess.run(["sha256sum", GGUF], capture_output=True, text=True).stdout.split()[0],
           "started_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    print("T1 placement + T3a split fit", flush=True)
    res["fit_split"] = fit("q8_0", "q4_0", "fit_split", 18081)   # its load log records n_ctx_slot at default verbosity; the T1 placement log came from a separate -lv 5 run (osc07/place_probe.sh)
    print("T2 quality", flush=True)
    res["f16"] = ppl("f16", "f16", "ppl_f16"); res["split"] = ppl("q8_0", "q4_0", "ppl_split")
    print("T3b L1 stack at -fitt 512", flush=True)
    res["fit_l1_q4_f512"] = fit("q4_0", "q4_0", "fit_l1_q4_f512", 18082, fitt=512)
    print("T4 speed", flush=True)
    res["bench_split"] = bench("q8_0", "q4_0", "bench_split")
    res["bench_q4"] = bench("q4_0", "q4_0", "bench_q4")
    res["ram_mb_end"] = S.ram()
    res["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, "kv_split.json"), "w"), indent=1)
    print("WROTE", os.path.join(OUT, "kv_split.json"))


if __name__ == "__main__":
    main()
