#!/usr/bin/env python3
"""KV-speed round: does the quantised-KV decode penalty grow with depth on the served 9B?

T1 llama-bench (full-cuda, -ngl 99 -fa 1 -ctk T -ctv T) for T in f16, q8_0, q4_0 at
   -d 0,4096,16384,32768, -p 512 -n 64 -r 5, after one discarded warm-up per type ->
   pp512 / tg64 mean +/- stddev per (T, depth).
T2 penalty per depth = 1 - X_T / X_f16 for both tests, 95 pct interval by the delta
   method (see penalty()). `--reparse` rebuilds the table from the raw logs on disk
   without re-running the GPU, for when the parse -- not the benchmark -- was wrong.
Caller stops the router and restores it; this script never touches it.
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
DEPTHS = [0, 4096, 16384, 32768]
OUT = paths.get_local("kv_speed_out_dir")
LOG = os.path.join(OUT, "logs")
T975_4 = 2.776445  # two-sided 97.5 pct Student-t point, 4 df (5 reps) -> 95 pct


def run(args, name, timeout=3600):
    os.makedirs(LOG, exist_ok=True)
    cmd = ["docker", "run", "--rm", "--gpus", "all", "-v", SCRATCH + ":/work",
           "--entrypoint", "/app/llama-bench", IMG] + args
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    out = p.stdout + p.stderr
    open(os.path.join(LOG, name + ".log"), "w").write(out)
    print("[%s] exit=%d secs=%.0f" % (name, p.returncode, time.time() - t0), flush=True)
    return p.returncode, out


def ram():
    return int(next(l for l in open("/proc/meminfo") if l.startswith("MemAvailable")).split()[1]) // 1024


def parse(out):
    """{'test@depth': [mean, sd, n]} -- llama-bench labels depth 0 with no `@ d0`."""
    rows = {}
    for line in out.splitlines():
        m = re.search(r"\|\s*(pp512|tg64)\s*(?:@\s*d(\d+))?\s*\|", line)
        if not m:
            continue
        d = int(m.group(2)) if m.group(2) else 0
        mm = re.match(r"([0-9.]+)\s*±\s*([0-9.]+)", [c.strip() for c in line.split("|")][-2])
        if mm:
            rows["%s@%d" % (m.group(1), d)] = [float(mm.group(1)), float(mm.group(2)), 5]
    return rows


def bench(tag):
    args = ["-m", "/work/Qwen3.5-9B-Q4_K_M.gguf", "-ngl", "99", "-fa", "1", "-ctk", tag,
            "-ctv", tag, "-p", "512", "-n", "64", "-d", ",".join(str(d) for d in DEPTHS)]
    run(args + ["-r", "1"], "bench_warm_" + tag)  # discarded; first rep is cold
    rc, out = run(args + ["-r", "5"], "bench_" + tag)
    return {"rc": rc, "rows": parse(out), "ram_mb": ram(), "loadavg": list(os.getloadavg()),
            "source_log": "logs/bench_%s.log" % tag}


def penalty(types):
    """P = 1 - X_T/X_f16; se_mean = sd/sqrt(5); se_P^2 = (se_T/mF)^2 + (mT*se_F/mF^2)^2;
    half-width = T975_4 * se_P. f16 is its own baseline: 0 +/- its own variance term."""
    out = {}
    for d in DEPTHS:
        r = {tag: {t: types[tag]["rows"].get("%s@%d" % (t, d)) for t in ("pp512", "tg64")}
             for tag in TYPES}
        for t in ("pp512", "tg64"):
            f = r["f16"][t]
            if not f or f[0] <= 0:
                continue
            se_f = f[1] / 5 ** 0.5
            for tag in TYPES:
                x = r[tag][t]
                if not x or x[0] <= 0:
                    continue
                se_p = ((x[1] / 5 ** 0.5 / f[0]) ** 2 + (x[0] * se_f / f[0] ** 2) ** 2) ** 0.5
                r[tag][t + "_penalty"] = 1.0 - x[0] / f[0]
                r[tag][t + "_hw"] = T975_4 * se_p
        out[str(d)] = r
    return out


def main():
    res = {"host": os.uname().nodename, "image": IMG, "depths": DEPTHS, "reps": 5, "types": {}}
    res["model_sha256"] = subprocess.run(["sha256sum", GGUF], capture_output=True, text=True).stdout.split()[0]
    res["ram_mb_start"], res["loadavg_start"] = ram(), list(os.getloadavg())
    if "--reparse" in sys.argv:
        for tag in TYPES:
            res["types"][tag] = {"rows": parse(open(os.path.join(LOG, "bench_%s.log" % tag)).read()),
                                 "source_log": "logs/bench_%s.log" % tag}
    else:
        res["started_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for tag in TYPES:
            res["types"][tag] = bench(tag)
            print(json.dumps({tag: res["types"][tag]["rows"]}), flush=True)
    res["penalties"] = penalty(res["types"])
    res["ram_mb_end"] = ram()
    res["loadavg_end"] = list(os.getloadavg())
    res["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    os.makedirs(OUT, exist_ok=True)
    json.dump(res, open(os.path.join(OUT, "kv_speed.json"), "w"), indent=1)
    print("WROTE", os.path.join(OUT, "kv_speed.json"))


if __name__ == "__main__":
    main()