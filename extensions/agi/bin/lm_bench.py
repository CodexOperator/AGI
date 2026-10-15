#!/usr/bin/env python3
"""lm_bench.py -- tenancy-instrumented wrapper around llama-bench.

Round 0 / chain 1 A1 tenancy protocol (hypothesis:lm-round0-box-calibration-and-two-kill-tests).

Every measurement row carries the box state it was taken under, because this
box is a shared VM whose load has already ranged 0.8 -> 16.6 within one day.
A tok/s number without its tenancy row is not evidence.

Usage:
    lm_bench.py --model PATH [--label NAME] [--threads 4] [--p 512] [--n 128]
                [--bench-bin PATH] [--outdir DIR] [--extra-arg ...]

Writes one JSONL line per llama-bench result row to
    <outdir>/<utc>.jsonl        (default outdir .agi/context/local-maxxing/bench)

Stdlib only. No installs. No git.
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

DEFAULT_OUTDIR = ".agi/context/local-maxxing/bench"


def utc_stamp():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def read_kb(path, key):
    try:
        with open(path) as fh:
            for line in fh:
                if line.startswith(key):
                    return int(line.split()[1])
    except OSError:
        pass
    return None


def loadavg():
    with open("/proc/loadavg") as fh:
        parts = fh.read().split()
    return {"l1": float(parts[0]), "l5": float(parts[1]), "l15": float(parts[2])}


def pgmajfault():
    return read_kb("/proc/vmstat", "pgmajfault")


def swap_free_kb():
    return read_kb("/proc/meminfo", "SwapFree")


def mem_available_kb():
    return read_kb("/proc/meminfo", "MemAvailable")


def top_rss(n=3):
    try:
        out = subprocess.run(
            ["ps", "-eo", "rss=,pid=,comm=", "--sort=-rss"],
            capture_output=True, text=True, timeout=10,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    procs = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        f = line.split(None, 2)
        if len(f) < 2:
            continue
        try:
            procs.append({"rss_kb": int(f[0]), "pid": int(f[1]),
                          "comm": f[2] if len(f) > 2 else ""})
        except ValueError:
            continue
        if len(procs) >= n:
            break
    return procs


def llama_commit(bench_bin):
    """Best-effort: llama-bench --version prints the build string."""
    for flag in ("--version", "-v"):
        try:
            r = subprocess.run([bench_bin, flag], capture_output=True,
                               text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        blob = (r.stdout or "") + (r.stderr or "")
        if blob.lstrip().lower().startswith("usage"):
            continue  # llama-bench rejects --version and prints usage
        m = re.search(r"\b([0-9a-f]{7,40})\b", blob)
        if m:
            return m.group(1)
        if blob.strip():
            return blob.strip().splitlines()[0][:120]
    return None


def parse_bench_json(stdout):
    """llama-bench -o json is an array; tolerate a {'results': [...]} dict."""
    txt = stdout.strip()
    if not txt:
        return []
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        # last-ditch: take the outermost [...] block
        i, j = txt.find("["), txt.rfind("]")
        if i < 0 or j <= i:
            return []
        try:
            data = json.loads(txt[i:j + 1])
        except json.JSONDecodeError:
            return []
    if isinstance(data, dict):
        data = data.get("results", [])
    return data if isinstance(data, list) else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--label", default=None)
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--p", type=int, default=512)
    ap.add_argument("--n", type=int, default=128)
    ap.add_argument("--bench-bin", default=None,
                    help="path to llama-bench (default: sibling of this tree)")
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--extra-arg", action="append", default=[])
    a = ap.parse_args()

    bench_bin = a.bench_bin or os.environ.get("LLAMA_BENCH", "llama-bench")
    model = os.path.abspath(a.model)
    model_bytes = os.path.getsize(model)
    ts = utc_stamp()

    # --- tenancy BEFORE ---
    before = {
        "loadavg": loadavg(),
        "mem_available_kb": mem_available_kb(),
        "swap_free_kb": swap_free_kb(),
        "pgmajfault": pgmajfault(),
        "top_rss": top_rss(3),
    }

    cmd = [bench_bin, "-m", model, "-t", str(a.threads),
           "-p", str(a.p), "-n", str(a.n), "-o", "json"] + a.extra_arg

    r = subprocess.run(cmd, capture_output=True, text=True)
    after = {
        "loadavg": loadavg(),
        "mem_available_kb": mem_available_kb(),
        "swap_free_kb": swap_free_kb(),
        "pgmajfault": pgmajfault(),
        "top_rss": top_rss(3),
    }
    delta = None
    if before["pgmajfault"] is not None and after["pgmajfault"] is not None:
        delta = after["pgmajfault"] - before["pgmajfault"]

    rows = parse_bench_json(r.stdout)
    if not rows:
        rows = [{"_no_result": True, "stderr": (r.stderr or "")[-800:],
                 "returncode": r.returncode}]

    outdir = os.path.join(os.getcwd(), a.outdir)
    os.makedirs(outdir, exist_ok=True)
    outpath = os.path.join(outdir, ts + ".jsonl")

    commit = llama_commit(bench_bin)
    # llama-bench has no --version; the JSON row carries the real commit.
    if rows and rows[0].get("build_commit"):
        commit = rows[0]["build_commit"]
    written = 0
    with open(outpath, "w") as fh:
        for row in rows:
            rec = {
                "ts_utc": ts,
                "llama_commit": commit,
                "label": a.label,
                "model_file": os.path.basename(model),
                "model_bytes": model_bytes,
                "threads": a.threads,
                # tenancy of the measurement, prepended:
                "loadavg_before": before["loadavg"],
                "loadavg_after": after["loadavg"],
                "mem_available_kb_before": before["mem_available_kb"],
                "mem_available_kb_after": after["mem_available_kb"],
                "swap_free_kb_before": before["swap_free_kb"],
                "swap_free_kb_after": after["swap_free_kb"],
                "pgmajfault_delta": delta,
                "top_rss_before": before["top_rss"],
                "top_rss_after": after["top_rss"],
                "cmd": " ".join(cmd),
            }
            # derive effective GB/s = tok/s * model bytes (bytes-touched ledger)
            tg = row.get("avg_ts") if row.get("n_gen") else None
            pp = row.get("avg_ts") if row.get("n_prompt") and not row.get("n_gen") else None
            if tg is not None:
                rec["eff_gbps_tg"] = round(tg * model_bytes / 1e9, 4)
            if pp is not None:
                rec["eff_gbps_pp"] = round(pp * model_bytes / 1e9, 4)
            rec["llama_bench_result"] = row
            fh.write(json.dumps(rec) + "\n")
            written += 1

    print(outpath)
    for row in rows:
        print("  %-28s %-22s %s" % (
            row.get("model_filename", os.path.basename(model))[:28],
            ("p%d n%d %s" % (row.get("n_prompt", a.p), row.get("n_gen", a.n),
                             row.get("test", "")))[:22],
            "avg_ts=%s stddev=%s" % (row.get("avg_ts"), row.get("stddev_ts")),
        ))
    print("  tenancy: load %s mem %s kB swap %s kB pgmajfault_delta=%s"
          % (before["loadavg"]["l1"], before["mem_available_kb"],
             before["swap_free_kb"], delta))
    print("  wrote %d row(s)" % written)
    return 0 if (rows and not rows[0].get("_no_result")) else 1


if __name__ == "__main__":
    sys.exit(main())
