#!/usr/bin/env python3
"""D1 CONJUNCT 2: does the ablation signal tell you WHICH bytes are cheap to drop?

Owns the SECOND conjunct of hypothesis:d1-random-set-mean-ablation:
    "...produces a measurable loss delta THAT PREDICTS THE BANDWIDTH-BOUND
     DECODE LEVER better than the unablated baseline."

Conjunct 1 (the delta is reproducible and above the batching noise floor) is
settled by experiment:a00-01a81f78-81defb and is NOT re-run here.

OPERATIONALIZATION (stated before the run)
------------------------------------------
The TM card records that on this box decode is bandwidth-bound (decode tok/s
>= single-process copy bandwidth). A decode lever is therefore a
BYTES-TOUCHED-PER-TOKEN reduction. The lever for an MLP intermediate unit:

    DROP the unit end to end  =  zero its gate_proj row, its up_proj row and
    its down_proj column. Params removed per unit =
        hidden_size (gate row) + hidden_size (up row) + hidden_size (down col)
        = 3 * 896 = 2688 params = 10752 bytes at fp32.
    bytes_removed_per_token = n_units_dropped * 10752   (each weight byte is
    read once per decoded token in the bandwidth-bound regime).

"Predicts better than no information":
  * no information = drop a RANDOM subset at byte budget B  -> drop_rand,
  * the ablation signal's recommendation = drop the LOWEST-importance units
    at the same budget B                                  -> drop_low,
  * positive control = drop the HIGHEST-importance units   -> drop_high.
  The signal PREDICTS iff loss(drop_low) < loss(drop_rand) < loss(drop_high)
  AND (loss(drop_rand) - loss(drop_low)) exceeds the across-seed spread of
  drop_rand. Otherwise the signal carries no droppable-byte information and
  the honest verdict is disproved / lean_disproved.

IMPORTANCE PROXY (first-order, and VALIDATED against measured single-unit drop)
    proxy_u = mean_abs_activation_u  *  ||down_proj.weight[:, u]||_2
This is the first-order magnitude of the residual-stream contribution lost when
unit u is dropped: a_u * W_down[:,u]. Its rank signal is validated by
measuring the ACTUAL single-unit drop delta for 10 highest-proxy and 10
lowest-proxy units on a reduced (2-window) eval, and reporting the rank
agreement (Spearman rho). If the proxy has no rank signal, that is reported.

BYTES ARE REMOVED BY ZEROING, NOT BY RESHAPING (honest limit):
the model keeps its shapes, so a real llama.cpp decode run on the zeroed model
would NOT read fewer bytes (zeros still occupy the tensors). The bytes figure
here is the PHYSICAL bytes that a shape-changing prune would remove; it is a
declared proxy for the lever. lm_bench.py was not run (a genuine bytes drop
requires re-conversion with changed per-layer intermediate_size, which a zeroed
model cannot express); this is stated, not hidden.

Usage:
    ~/.venv-lm/bin/python .agi/context/local-maxxing/d1/d1_predictiveness.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d1_ablation as A  # noqa: E402  (settled conjunct-1 machinery)

OUT_JSON = os.path.join(HERE, "d1_predictiveness_results.json")
FRACTION = 0.05
RAND_SEEDS = [0, 1, 2]
N_PROBE_HIGH = 10
N_PROBE_LOW = 10
PROBE_WINDOWS = 2  # reduced eval for the 20 single-unit probes (rank signal only)


def spearman(xs, ys):
    """Spearman rho with average ranks; no scipy."""
    x = np.asarray(xs, float)
    y = np.asarray(ys, float)
    rx = _rank(x)
    ry = _rank(y)
    rx = rx - rx.mean()
    ry = ry - ry.mean()
    denom = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / denom) if denom > 0 else float("nan")


def _rank(a):
    order = np.argsort(a, kind="mergesort")
    ranks = np.empty(len(a), float)
    ranks[order] = np.arange(len(a), dtype=float)
    # average ties
    sa = a[order]
    i = 0
    while i < len(sa):
        j = i
        while j + 1 < len(sa) and sa[j + 1] == sa[i]:
            j += 1
        if j > i:
            ranks[order[i:j + 1]] = (i + j) / 2.0
        i = j + 1
    return ranks


class UnitDropper:
    """Zero gate/up rows + down column for selected MLP intermediate units."""

    def __init__(self, model, n_layers):
        mods = dict(model.named_modules())
        self.mods = [
            (mods[f"model.layers.{i}.mlp.gate_proj"],
             mods[f"model.layers.{i}.mlp.up_proj"],
             mods[f"model.layers.{i}.mlp.down_proj"])
            for i in range(n_layers)
        ]
        self.saved = []

    @torch.no_grad()
    def drop(self, units, per_layer_units):
        for u in units:
            li = int(u) // per_layer_units
            ch = int(u) % per_layer_units
            gate, up, down = self.mods[li]
            g = gate.weight[ch].clone(); gate.weight[ch].zero_()
            self.saved.append((gate.weight, ch, "row", g))
            p = up.weight[ch].clone(); up.weight[ch].zero_()
            self.saved.append((up.weight, ch, "row", p))
            d = down.weight[:, ch].clone(); down.weight[:, ch].zero_()
            self.saved.append((down.weight, ch, "col", d))

    @torch.no_grad()
    def restore(self):
        for w, ch, kind, orig in self.saved:
            if kind == "row":
                w[ch].copy_(orig)
            else:
                w[:, ch].copy_(orig)
        self.saved = []


def main() -> int:
    t_start = time.time()
    report = {
        "script": os.path.abspath(__file__),
        "conjunct": "2 of 2: does the ablation signal predict the bandwidth-bound decode lever better than no information?",
        "model_id": A.MODEL_ID,
        "fraction": FRACTION,
        "rand_seeds": RAND_SEEDS,
        "unit_drop_definition": "zero gate_proj row + up_proj row + down_proj column for the unit",
        "bytes_per_unit_dropped": None,
        "box": {"start": A.box_load()},
    }

    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tok = AutoTokenizer.from_pretrained(A.MODEL_ID)
    try:
        model = AutoModelForCausalLM.from_pretrained(A.MODEL_ID, dtype=torch.float32)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(A.MODEL_ID, torch_dtype=torch.float32)
    model.eval()
    down_projs = A.find_down_projs(model)
    per_layer_units = down_projs[0][1].in_features
    n_layers = len(down_projs)
    total_units = per_layer_units * n_layers
    hidden = model.config.hidden_size
    bytes_per_unit = 3 * hidden * 4  # fp32
    k = int(round(FRACTION * total_units))
    report["model"] = {
        "revision": getattr(model.config, "_commit_hash", None),
        "n_layers": n_layers,
        "per_layer_units": per_layer_units,
        "hidden_size": hidden,
        "total_units": total_units,
    }
    report["bytes_per_unit_dropped"] = bytes_per_unit
    report["k_units"] = k
    report["bytes_removed_per_token"] = k * bytes_per_unit
    print(json.dumps(report["model"]), flush=True)
    print(f"k={k} units, {bytes_per_unit} bytes/unit, "
          f"{k * bytes_per_unit / 1e6:.1f} MB/token lever", flush=True)

    # ---------------- eval windows (identical to conjunct 1) ----------------
    from datasets import load_dataset
    ds = load_dataset(A.EVAL_DATASET, A.EVAL_CONFIG, split=A.EVAL_SPLIT)
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    ids = tok(text, return_tensors="pt").input_ids[0]
    need = A.N_WINDOWS * A.WINDOW
    ids = ids[:need]
    eval_hash = hashlib.sha256(ids.numpy().tobytes()).hexdigest()[:16]
    windows = [ids[i * A.WINDOW:(i + 1) * A.WINDOW].unsqueeze(0) for i in range(A.N_WINDOWS)]
    report["eval"] = {"token_hash": eval_hash, "expected_token_hash": "cafa6c30c6d28f7d",
                      "n_windows": A.N_WINDOWS, "window_tokens": A.WINDOW}
    assert eval_hash == "cafa6c30c6d28f7d", eval_hash
    batch4 = [torch.cat(windows[i:i + 4], dim=0) for i in range(0, A.N_WINDOWS, 4)]

    # ---------------- per-unit mean |activation| + column norms ----------------
    print("\n=== importance proxy ===", flush=True)
    t0 = time.time()
    sums = [torch.zeros(per_layer_units, dtype=torch.float64) for _ in down_projs]
    counts = [0]

    def mk_capture(i):
        def hook(module, args):
            x = args[0]
            sums[i] += x.detach().reshape(-1, x.shape[-1]).abs().sum(dim=0, dtype=torch.float64)
            if i == 0:
                counts[0] += x.shape[0] * x.shape[1]
        return hook

    handles = [m.register_forward_pre_hook(mk_capture(i)) for i, (_, m) in enumerate(down_projs)]
    try:
        A.forward_loss(model, [torch.cat(windows, dim=0)])
    finally:
        for h in handles:
            h.remove()
    mean_abs = torch.cat([(s / counts[0]).to(torch.float32) for s in sums])  # [total_units]
    col_norm = torch.cat([m.weight.detach().float().norm(dim=0) for _, m in down_projs])
    proxy = (mean_abs * col_norm)
    report["proxy"] = {
        "definition": "mean_abs_activation_u * L2(down_proj.weight[:,u])",
        "capture_wall_seconds": round(time.time() - t0, 2),
        "mean_abs_stats": {"min": float(mean_abs.min()), "max": float(mean_abs.max()),
                           "mean": float(mean_abs.mean())},
        "proxy_stats": {"min": float(proxy.min()), "max": float(proxy.max()),
                        "mean": float(proxy.mean()), "median": float(proxy.median())},
        "box": A.box_load(),
    }
    print(json.dumps(report["proxy"]["proxy_stats"]), flush=True)

    order = np.argsort(proxy.detach().numpy())
    highest = order[-N_PROBE_HIGH:][::-1]
    lowest = order[:N_PROBE_LOW]
    dropper = UnitDropper(model, n_layers)

    # ---------------- single-unit drop probes (2-window eval) ----------------
    print("\n=== single-unit drop probes (proxy rank validation) ===", flush=True)
    probe_windows = windows[:PROBE_WINDOWS]
    base2 = A.forward_loss(model, [torch.cat(probe_windows, dim=0)])
    probes = []
    for tag, ulist in (("high", highest), ("low", lowest)):
        for u in ulist:
            t0 = time.time()
            dropper.drop([int(u)], per_layer_units)
            try:
                loss = A.forward_loss(model, [torch.cat(probe_windows, dim=0)])
            finally:
                dropper.restore()
            row = {
                "proxy_rank": tag,
                "unit": int(u),
                "proxy": float(proxy[u]),
                "mean_abs": float(mean_abs[u]),
                "col_norm": float(col_norm[u]),
                "drop_loss_2win": loss,
                "drop_delta_2win": loss - base2,
                "wall_seconds": round(time.time() - t0, 2),
            }
            probes.append(row)
            print(json.dumps(row), flush=True)
    pr_delta = [r["drop_delta_2win"] for r in probes]
    pr_proxy = [r["proxy"] for r in probes]
    report["probes"] = {
        "probe_windows": PROBE_WINDOWS,
        "baseline_loss_2win": base2,
        "rows": probes,
        "spearman_proxy_vs_delta": spearman(pr_proxy, pr_delta),
        "mean_delta_high": float(np.mean([r["drop_delta_2win"] for r in probes if r["proxy_rank"] == "high"])),
        "mean_delta_low": float(np.mean([r["drop_delta_2win"] for r in probes if r["proxy_rank"] == "low"])),
    }
    print(f"spearman(proxy, single-unit delta) = {report['probes']['spearman_proxy_vs_delta']:.3f}", flush=True)

    # ---------------- conditions at the same byte budget ----------------
    print("\n=== conditions at 5% budget (structural drop) ===", flush=True)
    t0 = time.time()
    baseline_loss = A.forward_loss(model, batch4)
    report["baseline_loss"] = baseline_loss
    report["baseline_conjunct1_reference"] = 2.8835255205631256
    print(f"baseline(4-win batch) = {baseline_loss:.6f} "
          f"(conjunct-1 reference 2.88352552) wall={time.time()-t0:.1f}s", flush=True)

    conditions = []
    for name, units in (("drop_low", order[:k]),
                        ("drop_high", order[-k:])):
        t0 = time.time()
        dropper.drop([int(u) for u in units], per_layer_units)
        try:
            loss = A.forward_loss(model, batch4)
        finally:
            dropper.restore()
        row = {"condition": name, "seed": None, "n_units": len(units),
               "loss": loss, "delta": loss - baseline_loss,
               "wall_seconds": round(time.time() - t0, 2), "box": A.box_load()}
        conditions.append(row)
        print(json.dumps({kk: vv for kk, vv in row.items() if kk != "box"}), flush=True)
    for seed in RAND_SEEDS:
        rng = np.random.default_rng(seed)
        units = np.sort(rng.choice(total_units, size=k, replace=False))
        t0 = time.time()
        dropper.drop([int(u) for u in units], per_layer_units)
        try:
            loss = A.forward_loss(model, batch4)
        finally:
            dropper.restore()
        row = {"condition": "drop_rand", "seed": seed, "n_units": k,
               "loss": loss, "delta": loss - baseline_loss,
               "wall_seconds": round(time.time() - t0, 2), "box": A.box_load()}
        conditions.append(row)
        print(json.dumps({kk: vv for kk, vv in row.items() if kk != "box"}), flush=True)
    report["conditions"] = conditions

    # ---------------- prediction score / verdict ----------------
    d_low = [r["delta"] for r in conditions if r["condition"] == "drop_low"]
    d_high = [r["delta"] for r in conditions if r["condition"] == "drop_high"]
    d_rand = [r["delta"] for r in conditions if r["condition"] == "drop_rand"]
    assert len(d_low) == 1 and len(d_high) == 1 and len(d_rand) == len(RAND_SEEDS)
    rand_spread = float(max(d_rand) - min(d_rand))
    rand_mean = float(np.mean(d_rand))
    separation = rand_mean - d_low[0]
    ordering = bool(d_low[0] < rand_mean < d_high[0])
    report["prediction_score"] = {
        "delta_drop_low": d_low[0],
        "delta_drop_high": d_high[0],
        "delta_drop_rand_mean": rand_mean,
        "delta_drop_rand_seeds": d_rand,
        "rand_seed_spread": rand_spread,
        "conjunct1_mean_ablation_seed_spread": 0.015702,
        "ordering_low_lt_rand_lt_high": ordering,
        "separation_rand_minus_low": separation,
        "separation_over_rand_spread": (separation / rand_spread) if rand_spread > 0 else None,
        "separation_over_conjunct1_spread": separation / 0.015702,
    }
    if ordering and separation > rand_spread:
        verdict = "proved"
    elif not ordering and separation <= 0:
        verdict = "disproved"
    elif separation > 0:
        verdict = "inconclusive_lean_proved"
    else:
        verdict = "inconclusive_lean_disproved"
    report["summary"] = {"proposed_verdict": verdict}
    report["box"]["end"] = A.box_load()
    report["wall_seconds_total"] = round(time.time() - t_start, 2)

    with open(OUT_JSON, "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print(f"\nproposed verdict: {verdict}", flush=True)
    print(json.dumps(report["prediction_score"], indent=2, default=str), flush=True)
    print(f"wrote {OUT_JSON} (wall {report['wall_seconds_total']}s)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
