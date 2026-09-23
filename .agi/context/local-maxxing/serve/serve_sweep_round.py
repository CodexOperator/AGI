#!/usr/bin/env python3
"""OSC.08 serving sweep on the served 9B: T1 nsys timeline of one served request, T2 one-knob
llama-bench arms, T3 llama-perplexity on the numerics arms + the stack, T4 the stack of winners.
The caller stops the router first and restores it after; this script never touches it.
Stages: `python3 serve_sweep_round.py t1|t2|t3|t4`; every path via paths.get_local (rule 13)."""
import json, os, re, sqlite3, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = HERE
while not os.path.isfile(os.path.join(ROOT, ".agi/config.json")): ROOT = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing")); sys.path.insert(0, os.path.join(ROOT, ".agi/context/local-maxxing/kv"))
import paths, kv_speed_round as S
IMG = "ghcr.io/ggml-org/llama.cpp:full-cuda"; NS = "/data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2"
SC = "/data/ml/scratch/osc02"; M = "/work/Qwen3.5-9B-Q4_K_M.gguf"; OUT = paths.get_local("serving_sweep_out_dir"); LOG = OUT + "/logs"; T975 = S.T975_4
os.makedirs(LOG, exist_ok=True)
BASE = ["-m", M, "-ngl", "99", "-fa", "1", "-ctk", "f16", "-ctv", "f16", "-p", "512", "-n", "64", "-d", "0,4096"]
ARMS = {"base": ([], {}), "fa0": (["-fa", "0"], {}), "kv_q8": (["-ctk", "q8_0", "-ctv", "q8_0"], {}), "kv_q4": (["-ctk", "q4_0", "-ctv", "q4_0"], {}), "kv_split": (["-ctk", "q8_0", "-ctv", "q4_0"], {}), "ub256": (["-ub", "256"], {}), "ub1024": (["-ub", "1024"], {}), "nograph": ([], {"GGML_CUDA_DISABLE_GRAPHS": "1"}), "mmq": ([], {"GGML_CUDA_FORCE_MMQ": "1"}), "cublas": ([], {"GGML_CUDA_FORCE_CUBLAS": "1"}), "t4": (["-t", "4"], {}), "t8": (["-t", "8"], {}), "t16": (["-t", "16"], {}), "mmp0": (["-mmp", "0"], {}), "mlock": (["--mlock"], {})}
NLL = {"base": ["-fa", "on", "-ctk", "f16", "-ctv", "f16"], "fa0": ["-fa", "off", "-ctk", "f16", "-ctv", "f16"], "kv_q8": ["-fa", "on", "-ctk", "q8_0", "-ctv", "q8_0"], "kv_q4": ["-fa", "on", "-ctk", "q4_0", "-ctv", "q4_0"], "kv_split": ["-fa", "on", "-ctk", "q8_0", "-ctv", "q4_0"], "mmq": ["-fa", "on", "-ctk", "f16", "-ctv", "f16"], "cublas": ["-fa", "on", "-ctk", "f16", "-ctv", "f16"]}
GROUPS = {"ub": ["ub256", "ub1024"], "t": ["t4", "t8", "t16"], "mmq": ["mmq"], "cublas": ["cublas"], "nograph": ["nograph"], "mmp0": ["mmp0"], "mlock": ["mlock"]}


def sh(cmd, name=None, timeout=3600):
    t0 = time.time(); p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    out = p.stdout + p.stderr
    if name: open(os.path.join(LOG, name + ".log"), "w").write(out)
    print("[%s] exit=%d %.0fs ram=%d" % (name or cmd[2], p.returncode, time.time() - t0, S.ram()), flush=True)
    return p.returncode, out


def dk(entry, args, name, env=None, mounts=None):
    e = sum([["-e", k + "=" + v] for k, v in (env or {}).items()], [])
    return sh(["docker", "run", "--rm", "--gpus", "all", "-v", SC + ":/work", "-v", OUT + ":/out"] + (["-v", NS + ":/nsys:ro"]) * (mounts == "nsys") + e + ["--entrypoint", entry if entry.startswith("/") else "/app/" + entry, IMG] + args, name)


def bench(n, fl, ev): return {"rows": S.parse(dk("llama-bench", BASE + ["-r", str(S.REPS)] + fl, n, ev)[1], S.REPS), "flags": fl, "env": ev}  # -r made explicit: llama-bench's default, 5


def ppl(n, fl, ev): m = re.findall(r"PPL\s*=\s*([0-9.]+)", dk("llama-perplexity", ["-m", M, "-f", "/work/wikitext-2-raw/wiki.test.raw", "-c", "512", "--chunks", "40", "-ngl", "99", "--seed", "42", "-t", "8", "--no-warmup"] + fl, n, ev)[1]); return {"ppl": float(m[-1]) if m else None, "flags": fl}


def gain(x, b): return (x[0] - b[0]) / b[0], T975 * ((x[1] / S.REPS ** .5 / b[0]) ** 2 + (x[0] * b[1] / S.REPS ** .5 / b[0] ** 2) ** 2) ** .5


def load(): return json.load(open(OUT + "/sweep.json")) if os.path.exists(OUT + "/sweep.json") else {}


def save(d):
    old = load(); old.update(d); os.makedirs(OUT, exist_ok=True); json.dump(old, open(OUT + "/sweep.json", "w"), indent=1); print("WROTE", OUT, list(d), flush=True)


def t1():
    open(SC + "/t1_req.json", "w").write(json.dumps({"prompt": open(SC + "/wikitext-2-raw/wiki.test.raw").read()[:9000], "max_tokens": 128, "temperature": 0}))
    N = "/nsys/target-linux-x64/nsys"   # the NS dir is bind-mounted read-only at /nsys in the container
    W = ("#!/bin/bash\n" + N + " profile --trace=cuda,osrt,nvtx --output=/out/nsys_prof --force-overwrite=true --sample=none "
         "/app/llama-server --cache-reuse 8 --host 0.0.0.0 --jinja --alias Qwen3.5-9B-Q4_K_M --fit on --model /work/Qwen3.5-9B-Q4_K_M.gguf --parallel 1 --port 18091 -fa on -ctk f16 -ctv f16 >/out/t1_server.log 2>&1 & pid=$!\n"
         "ok=0; for i in $(seq 1 300); do curl -sf 127.0.0.1:18091/health >/dev/null && { ok=1; break; }; sleep 1; done; echo \"health_ok=$ok load_s=$i\" > /out/t1_health.txt\n"
         "if [ $ok = 1 ]; then curl -s 127.0.0.1:18091/v1/completions -H 'Content-Type: application/json' -d @/work/t1_req.json -o /out/t1_completion.json; curl -s 127.0.0.1:18091/slots -o /out/t1_slots.json; fi\n"
         "sleep 3; kill -INT $pid; wait $pid\n"
         + N + " stats --report cuda_gpu_kern_sum,cuda_gpu_mem_size_sum,cuda_gpu_mem_time_sum,osrt_sum --format csv --output /out/nsys /out/nsys_prof.nsys-rep >/out/nsys_stats.txt 2>&1\n"
         + N + " export --type sqlite --output /out/nsys_prof.sqlite /out/nsys_prof.nsys-rep >>/out/nsys_stats.txt 2>&1\n")
    open(SC + "/t1_wrapper.sh", "w").write(W)
    dk("/bin/bash", ["/work/t1_wrapper.sh"], "t1", mounts="nsys")
    iv = sorted((int(a), int(b)) for a, b in sqlite3.connect(OUT + "/nsys_prof.sqlite").execute("select start,end from CUPTI_ACTIVITY_KIND_KERNEL")) if os.path.exists(OUT + "/nsys_prof.sqlite") else []
    if not iv: print("NO SQLITE -> no window stats", flush=True); return
    t1_analyze(iv)


def t1_analyze(iv=None):
    """Windows from the request's own timings: the decode burst is the densest kernel cluster in the
    last 20 s; prefill is the prompt_ms+d predicted_ms span that ends where decode ends."""
    if iv is None: iv = sorted((int(a), int(b)) for a, b in sqlite3.connect(OUT + "/nsys_prof.sqlite").execute("select start,end from CUPTI_ACTIVITY_KIND_KERNEL"))
    tm = json.load(open(OUT + "/t1_completion.json"))["timings"]
    t_end = max(b for a, b in iv); d, cl, cur = [x for x in iv if x[1] > t_end - 20e9], [], []
    for a, b in d:
        if cur and a - cur[-1][1] > 5e8: cl.append(cur); cur = []
        cur.append((a, b))
    cl.append(cur); dec = max(cl, key=len); d0, d1 = dec[0][0], dec[-1][1]
    r0 = d1 - int((tm["prompt_ms"] + tm["predicted_ms"]) * 1e6)

    def busy(lo, hi):
        m = []
        for a, b in iv:
            if b > lo and a < hi:
                a, b = max(a, lo), min(b, hi)
                if m and a <= m[-1][1]: m[-1][1] = max(m[-1][1], b)
                else: m.append([a, b])
        return sum(b - a for a, b in m)

    w = {k: {"span_s": round((hi - lo) / 1e9, 2), "gpu_busy_s": round(busy(lo, hi) / 1e9, 2), "gpu_busy_frac": round(busy(lo, hi) / (hi - lo), 3)} for k, lo, hi in [("prefill", r0, d0), ("decode", d0, d1), ("request", r0, d1)]}
    w.update({"decode_kernels": len(dec), "prompt_n": tm["prompt_n"], "prompt_ms": tm["prompt_ms"], "predicted_ms": tm["predicted_ms"], "prompt_per_second": tm["prompt_per_second"], "predicted_per_second": tm["predicted_per_second"], "sqlite_mb": os.path.getsize(OUT + "/nsys_prof.sqlite") / 1e6})
    json.dump(w, open(OUT + "/nsys_window.json", "w"), indent=1); print("WROTE nsys_window.json", json.dumps(w), flush=True)


def t2():
    res = {}
    for n, (fl, ev) in ARMS.items(): res[n] = bench(n, fl, ev); print(n, json.dumps(res[n]["rows"]), flush=True)
    save({"t2": res})


def t3(): save({"t3": {n: ppl("ppl_" + n, fl, {}) for n, fl in NLL.items()}})


def t4():
    d = load(); rows, nr = {k: v["rows"] for k, v in d["t2"].items()}, {k: v["ppl"] for k, v in d["t3"].items()}
    b, bn = rows["base"]["tg64@4096"], nr["base"]; wins, table = [], {}
    for n in ARMS:
        if n == "base" or not rows.get(n, {}).get("tg64@4096"): continue
        g, hw = gain(rows[n]["tg64@4096"], b); p = nr.get(n); nu = p is not None and abs(p - bn) / bn * 100 <= 0.01
        table[n] = {"gain": g, "hw": hw, "nll_pct": None if p is None else (p - bn) / bn * 100, "nll_held": nu}
        if g - hw > 0 and (p is None or nu) and any(n in v for v in GROUPS.values()): wins.append(n)
    fl = sum([ARMS[n][0] for n in wins], []); ev = {k: v for n in wins for k, v in ARMS[n][1].items()}
    stack = bench("stack", fl, ev) if wins else {"rows": {}, "flags": []}
    st = ppl("ppl_stack", NLL["base"], ev)
    row = stack["rows"].get("tg64@4096")
    save({"t4": {"winners": wins, "flags": fl, "env": ev, "table": table, "stack_bench": stack, "stack_tg64@4096": row, "stack_gain": None if not row else list(gain(row, b)), "stack_ppl": st}})


if __name__ == "__main__":
    {"t1": t1, "t1r": t1_analyze, "t2": t2, "t3": t3, "t4": t4}[sys.argv[1]]()
