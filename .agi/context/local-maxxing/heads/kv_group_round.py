#!/usr/bin/env python3
"""T2-T4 round: baseline, 32 single (layer, KV-group) zero-ablations, then a joint
greedy curve. Every llama-perplexity run is fully on the GPU inside the
llama.cpp full-cuda container with identical flags; the GGUF is a scratch copy
patched by kv_group_surgery.py and restored between runs. Stdlib only.
"""
import csv, json, math, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paths
from kv_group_surgery import MODEL, layer_tensors, GGUF, patch, restore, tensor_sha

LAYERS = [3, 7, 11, 15, 19, 23, 27, 31]
MODELS_DIR = "/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf"
WIKITEXT = "/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw"
OUT = paths.get_local("kv_groups_dir")
LOGS = os.path.join(OUT, "logs")
CMD = ["docker", "run", "--rm", "--gpus", "all", "-v", "/data/ml/scratch/osc02:/work",
       "--entrypoint", "/app/llama-perplexity", "ghcr.io/ggml-org/llama.cpp:full-cuda",
       "-m", "/work/Qwen3.5-9B-Q4_K_M.gguf", "-f", "/work/wikitext-2-raw/wiki.test.raw",
       "-c", "512", "--chunks", "40", "-ngl", "99", "-fa", "off", "--seed", "42", "-t", "8",
       "--no-warmup"]
DEADLINE = float(os.environ.get("KV_ROUND_DEADLINE", "0"))


def ram_avail():
    with open("/proc/meminfo") as f:
        for line in f:
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) // 1024
    return -1


def run(tag):
    log = os.path.join(LOGS, tag + ".log")
    t0 = time.time()
    with open(log, "w") as fh:
        rc = subprocess.call(CMD, stdout=fh, stderr=subprocess.STDOUT)
    ppl = None
    for line in open(log, errors="replace"):
        if "Final estimate: PPL" in line:
            ppl = float(line.rsplit("PPL =", 1)[1].split()[0])
    return {"tag": tag, "ppl": ppl, "rc": rc, "secs": round(time.time() - t0, 1),
            "ram_avail_mb": ram_avail(), "log": os.path.basename(log)}


def main():
    os.makedirs(LOGS, exist_ok=True)
    lt = layer_tensors(GGUF(MODEL))
    assert sorted(lt) == LAYERS, sorted(lt)
    tour = []
    for L in LAYERS:
        restore(L)

    t2 = [run("baseline_1"), run("baseline_2")]
    base = t2[0]["ppl"]
    assert base, "no baseline ppl"
    nll_base = math.log(base)

    rows, t0 = [], time.time()
    for L in LAYERS:
        for g in range(4):
            if DEADLINE and time.time() - t0 > DEADLINE:
                break
            restore(L)
            patch(L, [g])
            r = run("single_L%d_g%d" % (L, g))
            r.update(layer=L, group=g)
            r["delta_nll"] = math.log(r["ppl"] / base) if r["ppl"] else None
            r["delta_nll_frac"] = (r["delta_nll"] / nll_base) if r["ppl"] else None
            rows.append(r)
            print(r["tag"], r["ppl"], r["delta_nll_frac"], flush=True)
        else:
            continue
        break
    for L in LAYERS:
        restore(L)

    singles = sorted([r for r in rows if r["delta_nll"] is not None],
                     key=lambda r: r["delta_nll"])
    curve, chosen = [{"k": 0, "ppl": base, "delta_nll": 0.0, "delta_nll_frac": 0.0,
                      "groups": []}], []
    for k, r in enumerate(singles, 1):
        if DEADLINE and time.time() - t0 > DEADLINE:
            break
        chosen.append((r["layer"], r["group"]))
        for L in LAYERS:
            restore(L)
        by_layer = {}
        for L, g in chosen:
            by_layer.setdefault(L, []).append(g)
        for L, gs in by_layer.items():
            patch(L, gs)
        rj = run("joint_%02d_%s" % (k, "_".join("L%dg%d" % p for p in chosen)))
        rj["k"] = k
        rj["groups"] = ["L%dg%d" % p for p in chosen]
        rj["delta_nll"] = math.log(rj["ppl"] / base)
        rj["delta_nll_frac"] = rj["delta_nll"] / nll_base
        curve.append(rj)
        print("joint", k, rj["ppl"], rj["delta_nll_frac"], flush=True)
        if rj["delta_nll_frac"] > 0.02:
            break
    for L in LAYERS:
        restore(L)

    shas = {str(L): tensor_sha(L) for L in LAYERS}
    orig = {str(L): open(os.path.join("/data/ml/scratch/osc02", "orig_L%d.q4k.sha256" % L)).read().strip()
            for L in LAYERS}
    k1 = sum(1 for c in curve if c["k"] and c["delta_nll_frac"] <= 0.01)
    k2 = sum(1 for c in curve if c["k"] and c["delta_nll_frac"] <= 0.02)
    kv_bytes_per_token = len(LAYERS) * 4 * 256 * 2 * 2
    doc = {
        "baseline_ppl": base, "baseline_runs": t2, "nll_base": nll_base,
        "singles": rows, "curve": curve,
        "k_1pct": k1, "k_2pct": k2,
        "kv_bytes_per_token_f16": kv_bytes_per_token,
        "context_multiplier_at_1pct": 32 / (32 - k1) if k1 < 32 else None,
        "context_multiplier_at_2pct": 32 / (32 - k2) if k2 < 32 else None,
        "determinism": t2[0]["ppl"] == t2[1]["ppl"],
        "tensor_shas_after": shas, "tensor_shas_original": orig,
        "tensor_restored": shas == orig,
        "orig_gguf_sha256": open("/data/ml/scratch/osc02/orig.sha256").read().split()[0],
        "command": " ".join(CMD),
        "wall_secs": round(time.time() - t0, 1),
    }
    with open(os.path.join(OUT, "kv_groups.json"), "w") as fh:
        json.dump(doc, fh, indent=1)
    with open(os.path.join(OUT, "singles.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["layer", "group", "ppl", "delta_nll",
                                           "delta_nll_frac", "secs", "ram_avail_mb", "tag"])
        w.writeheader()
        for r in sorted(rows, key=lambda r: r["delta_nll"]):
            w.writerow({k: r[k] for k in w.fieldnames})
    with open(os.path.join(OUT, "curve.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["k", "groups", "ppl", "delta_nll", "delta_nll_frac", "secs", "ram_avail_mb"])
        for c in curve:
            w.writerow([c["k"], " ".join(c["groups"]), c["ppl"], c["delta_nll"],
                        c["delta_nll_frac"], c.get("secs"), c.get("ram_avail_mb")])
    print(json.dumps({k: doc[k] for k in ("baseline_ppl", "determinism", "k_1pct", "k_2pct",
                                          "kv_bytes_per_token_f16", "tensor_restored",
                                          "context_multiplier_at_1pct")}, indent=1))


if __name__ == "__main__":
    main()
