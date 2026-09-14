#!/usr/bin/env python3
"""D1 mean-ablation loss measurement on Qwen2.5-0.5B (CPU only).

WHAT THIS MEASURES
------------------
Does a FIXED random subset of "byte-neurons" -- mean-ablated -- produce a
reproducible loss delta above a PREDEFINED noise threshold?

This script owns the FIRST conjunct of hypothesis:d1-random-set-mean-ablation.
It deliberately does NOT touch lm_bench.py or the bandwidth-bound decode lever;
a sibling kid owns the second conjunct.

UNIT DEFINITION ("byte-neuron")
------------------------------
Qwen2.5-0.5B's MLP block is SwiGLU:  down_proj( act(gate_proj(x)) * up_proj(x) ).
A "byte-neuron" is one INPUT CHANNEL of `down_proj` for one layer: i.e. one
intermediate MLP unit. Per layer the unit count is `intermediate_size`; layers
are flattened into ONE index space in layer order, so unit index
    u in [0, num_hidden_layers * intermediate_size)
maps to (layer = u // intermediate_size, channel = u % intermediate_size).

Why this unit: the residual-stream alternative (hidden_size channels) has only
896 units and each is heavily entangled with attention output, so ablating one
is not "a neuron"; the MLP intermediate channel is the smallest unit with a
private scalar activation and a 1:1 write into the residual stream. This is the
standard reading of "neuron" for a transformer MLP.

MEAN-ABLATION
-------------
For each selected unit we replace its activation during the forward pass with
the mean activation that unit takes over the fixed eval/calibration set,
computed once and cached. Mechanism: a `forward_pre_hook` on every `down_proj`
module rewrites args[0][..., channel] in place for the selected channels. The
mean is computed by a separate forward pass with capture hooks.

NOISE THRESHOLD -- DEFINED BEFORE ANY ABLATION NUMBER IS TAKEN
--------------------------------------------------------------
Baseline (0% ablation) is run REPEAT times over the SAME eval set, each repeat
using a different batch shape (1 / 4 / 8 windows per forward) so the batched
matmul reduction order genuinely differs between repeats. Then:

    baseline_spread = max(baseline_loss) - min(baseline_loss)
    noise_threshold = max(baseline_spread, 1e-12)

`noise_threshold` is computed from baseline data only, is written into the
results JSON, and every delta is also reported as `delta / noise_threshold`.
We also report the eval-set sampling figure `stderr_mean` (std of per-window
losses / sqrt(n_windows)) as INFORMATION ONLY -- it is not the threshold,
because baseline and ablated losses are measured on the identical fixed token
set, so eval-set sampling variance cancels in the difference.

RESULT TAXONOMY (proposed honestly by this script)
--------------------------------------------------
proved        : every fraction's delta exceeds the threshold for EVERY seed.
disproved     : delta within the threshold.
lean_*:N      : otherwise (N = integer percent).

Usage:
    ~/.venv-lm/bin/python .agi/context/local-maxxing/d1/d1_ablation.py
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from datetime import datetime, timezone

import numpy as np
import torch

MODEL_ID = "Qwen/Qwen2.5-0.5B"
EVAL_DATASET = "wikitext"
EVAL_CONFIG = "wikitext-2-raw-v1"
EVAL_SPLIT = "test"
N_WINDOWS = 8
WINDOW = 512
FRACTIONS = [0.05, 0.20]
SEEDS = [0, 1, 2]
BASELINE_BATCH_SHAPES = [1, 4, 8]  # "different batch orderings" = different reduction order

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, "d1_ablation_results.json")
MEAN_CACHE = os.path.join(HERE, "d1_mean_activations.npz")


def box_load() -> dict:
    """Tenancy row: a number without its load is not evidence."""
    la = os.getloadavg()
    mem = {}
    with open("/proc/meminfo") as fh:
        for line in fh:
            k, _, v = line.partition(":")
            if k in ("MemAvailable", "MemTotal"):
                mem[k] = int(v.strip().split()[0])
    return {
        "loadavg_1_5_15": [round(x, 3) for x in la],
        "mem_available_kb": mem.get("MemAvailable"),
        "mem_total_kb": mem.get("MemTotal"),
        "nproc": os.cpu_count(),
        "utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def pip_freeze() -> list[str]:
    try:
        out = subprocess.run(
            [sys.executable, "-m", "pip", "freeze"],
            capture_output=True, text=True, timeout=120, check=False,
        ).stdout
        return [l for l in out.splitlines() if l.strip()]
    except Exception as exc:  # pragma: no cover - evidence best effort
        return [f"<pip freeze failed: {exc}>"]


def find_down_projs(model):
    """All modules whose name ends in `down_proj`, in NUMERIC layer order.

    Plain string sort is wrong here: 'model.layers.10...' < 'model.layers.2...'.
    """
    mods = [(n, m) for n, m in model.named_modules() if n.endswith("down_proj")]

    def layer_idx(nm):
        try:
            return int(nm.split(".layers.")[1].split(".")[0])
        except (IndexError, ValueError):
            return 1 << 30

    mods.sort(key=lambda nm: layer_idx(nm[0]))
    return mods


@torch.no_grad()
def forward_loss(model, batches, ablator=None):
    """Mean loss over batches. batches: list of LongTensor [B, W]."""
    total, ntok = 0.0, 0
    for ids in batches:
        if ablator is not None:
            ablator.arm(ids.shape[0])
        out = model(input_ids=ids, labels=ids)
        n = ids.numel()
        total += float(out.loss) * n
        ntok += n
    if ablator is not None:
        ablator.disarm()
    return total / ntok


class MeanAblator:
    """forward_pre_hook that replaces selected down_proj input channels with
    the cached per-unit mean, only on the selected layers."""

    def __init__(self, down_projs, mean_per_layer, selected_by_layer, mask_by_layer):
        self.handles = []
        for i, (_, mod) in enumerate(down_projs):
            if selected_by_layer[i] is None or len(selected_by_layer[i]) == 0:
                continue
            ch = torch.as_tensor(selected_by_layer[i], dtype=torch.long)
            mean = mean_per_layer[i].index_select(0, ch)  # [k]
            self.handles.append(
                mod.register_forward_pre_hook(self._make(ch, mean))
            )

    @staticmethod
    def _make(ch, mean):
        def hook(module, args):
            x = args[0]
            # x: [..., intermediate_size]; channel index is the last dim
            view = x.view(-1, x.shape[-1])
            view.index_copy_(1, ch, mean.unsqueeze(0).expand(view.shape[0], -1))
            args = (x,) + tuple(args[1:])
            return args
        return hook

    def arm(self, batch_size):  # kept for symmetry with the capture pass
        return None

    def disarm(self):
        return None

    def remove(self):
        for h in self.handles:
            h.remove()
        self.handles = []


def main() -> int:
    t_start = time.time()
    report = {
        "script": os.path.abspath(__file__),
        "model_id": MODEL_ID,
        "unit_definition": (
            "MLP down_proj input channel (intermediate MLP unit), per layer; "
            "layers flattened in order into one index space"
        ),
        "unit_index_space_size": None,
        "eval": {
            "dataset": EVAL_DATASET,
            "config": EVAL_CONFIG,
            "split": EVAL_SPLIT,
            "n_windows": N_WINDOWS,
            "window_tokens": WINDOW,
            "total_tokens": N_WINDOWS * WINDOW,
        },
        "fractions": FRACTIONS,
        "seeds": SEEDS,
        "baseline_batch_shapes": BASELINE_BATCH_SHAPES,
        "box": {"start": box_load()},
        "env": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "torch": torch.__version__,
            "numpy": np.__version__,
            "transformers": None,
        },
        "argv": sys.argv,
    }

    import transformers
    from transformers import AutoModelForCausalLM, AutoTokenizer

    report["env"]["transformers"] = transformers.__version__
    print("pip freeze (recorded into JSON)...", flush=True)
    report["pip_freeze"] = pip_freeze()

    # ---------------- model ----------------
    t0 = time.time()
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    try:
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, dtype=torch.float32)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float32)
    model.eval()
    cfg = model.config
    n_params = sum(p.numel() for p in model.parameters())
    down_projs = find_down_projs(model)
    per_layer_units = down_projs[0][1].in_features if down_projs else None
    total_units = per_layer_units * len(down_projs)
    report["model"] = {
        "revision": getattr(cfg, "_commit_hash", None),
        "num_hidden_layers": getattr(cfg, "num_hidden_layers", None),
        "intermediate_size": getattr(cfg, "intermediate_size", None),
        "hidden_size": getattr(cfg, "hidden_size", None),
        "num_params": n_params,
        "n_down_proj_modules": len(down_projs),
        "down_proj_in_features": per_layer_units,
        "load_seconds": round(time.time() - t0, 2),
    }
    report["unit_index_space_size"] = total_units
    print(json.dumps(report["model"], indent=2), flush=True)
    assert per_layer_units == cfg.intermediate_size, (per_layer_units, cfg.intermediate_size)
    assert len(down_projs) == cfg.num_hidden_layers

    # ---------------- eval windows ----------------
    from datasets import load_dataset

    ds = load_dataset(EVAL_DATASET, EVAL_CONFIG, split=EVAL_SPLIT)
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    ids = tok(text, return_tensors="pt").input_ids[0]
    need = N_WINDOWS * WINDOW
    if ids.numel() < need:
        raise SystemExit(f"eval corpus too small: {ids.numel()} < {need}")
    ids = ids[:need]
    eval_hash = hashlib.sha256(ids.numpy().tobytes()).hexdigest()[:16]
    windows = [ids[i * WINDOW:(i + 1) * WINDOW].unsqueeze(0) for i in range(N_WINDOWS)]
    report["eval"]["dataset_revision"] = getattr(ds, "_fingerprint", None)
    report["eval"]["token_hash"] = eval_hash
    report["eval"]["tokenizer_hash"] = hashlib.sha256(
        json.dumps(tok.get_vocab(), sort_keys=True).encode()
    ).hexdigest()[:16]

    def batches_for(order_seed: int, batch_size: int):
        order = np.random.default_rng(order_seed).permutation(N_WINDOWS)
        w = [windows[i] for i in order]
        return [torch.cat(w[i:i + batch_size], dim=0) for i in range(0, N_WINDOWS, batch_size)]

    # ---------------- noise threshold (baseline only, BEFORE ablation) ----------------
    print("\n=== baseline / noise threshold ===", flush=True)
    # per-window losses computed ONCE, batch_size=1 -- reused as the eval-set
    # spread figure. Each repeat's baseline_loss is its own batched forward pass.
    t0 = time.time()
    per_window_losses = [forward_loss(model, [windows[i]]) for i in range(N_WINDOWS)]
    per_window_seconds = round(time.time() - t0, 2)
    baseline = []
    for bs in BASELINE_BATCH_SHAPES:
        t0 = time.time()
        bl = forward_loss(model, batches_for(order_seed=100 + bs, batch_size=bs))
        row = {
            "batch_size": bs,
            "order_seed": 100 + bs,
            "baseline_loss": bl,
            "wall_seconds": round(time.time() - t0, 2),
            "box": box_load(),
        }
        baseline.append(row)
        print(json.dumps({k: v for k, v in row.items() if k != "box"}), flush=True)

    bl_losses = [r["baseline_loss"] for r in baseline]
    baseline_loss = float(np.mean(bl_losses))
    baseline_spread = float(max(bl_losses) - min(bl_losses))
    pw = np.array(per_window_losses)
    stderr_mean = float(pw.std(ddof=1) / np.sqrt(len(pw))) if len(pw) > 1 else 0.0
    noise_threshold = max(baseline_spread, 1e-12)
    report["baseline"] = {
        "runs": baseline,
        "per_window_losses": [float(x) for x in per_window_losses],
        "per_window_seconds": per_window_seconds,
        "baseline_loss": baseline_loss,
        "baseline_spread": baseline_spread,
        "stderr_mean_information_only": stderr_mean,
        "noise_threshold": noise_threshold,
        "noise_threshold_definition": (
            "max over baseline repeat losses minus min over baseline repeat losses; "
            "repeats differ only in batch shape (1/4/8 windows per forward), so the "
            "spread measures float/batching reproducibility of the identical token set"
        ),
    }
    print(f"baseline_loss={baseline_loss:.6f} spread={baseline_spread:.3e} "
          f"noise_threshold={noise_threshold:.3e}", flush=True)

    # ---------------- mean activations (cached) ----------------
    print("\n=== mean activations ===", flush=True)
    t0 = time.time()
    mean_per_layer = None
    cache_hit = False
    if os.path.exists(MEAN_CACHE):
        z = np.load(MEAN_CACHE, allow_pickle=False)
        if str(z.get("eval_hash")) == eval_hash and int(z["n_layers"]) == len(down_projs):
            mean_per_layer = [torch.from_numpy(z[f"L{i}"]) for i in range(len(down_projs))]
            cache_hit = True
            print("loaded cached means", flush=True)
    if mean_per_layer is None:
        sums = [torch.zeros(per_layer_units, dtype=torch.float64) for _ in down_projs]
        counts = [0]

        def make_capture(i):
            def hook(module, args):
                x = args[0]
                sums[i] += x.detach().reshape(-1, x.shape[-1]).sum(dim=0, dtype=torch.float64)
                if i == 0:
                    counts[0] += x.shape[0] * x.shape[1]
            return hook

        handles = [m.register_forward_pre_hook(make_capture(i)) for i, (_, m) in enumerate(down_projs)]
        try:
            forward_loss(model, [torch.cat(windows, dim=0)])
        finally:
            for h in handles:
                h.remove()
        mean_per_layer = [(s / counts[0]).to(torch.float32) for s in sums]
        np.savez(
            MEAN_CACHE,
            eval_hash=eval_hash,
            n_layers=len(down_projs),
            **{f"L{i}": mean_per_layer[i].numpy() for i in range(len(down_projs))},
        )
        print("computed + cached means", flush=True)
    report["mean_activation"] = {
        "calibration_set": "the fixed eval set itself (same 4096 tokens)",
        "cache_path": MEAN_CACHE,
        "cache_hit": cache_hit,
        "wall_seconds": round(time.time() - t0, 2),
        "box": box_load(),
    }

    # ---------------- ablation sweep ----------------
    print("\n=== ablation sweep ===", flush=True)
    results = []
    for frac in FRACTIONS:
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            k = int(round(frac * total_units))
            sel = np.sort(rng.choice(total_units, size=k, replace=False))
            sel_by_layer = [[] for _ in down_projs]
            for u in sel:
                sel_by_layer[u // per_layer_units].append(int(u % per_layer_units))
            sel_hash = hashlib.sha256(sel.tobytes()).hexdigest()[:16]

            ablator = MeanAblator(down_projs, mean_per_layer, sel_by_layer, None)
            t0 = time.time()
            try:
                abl_loss = forward_loss(model, batches_for(order_seed=200 + seed, batch_size=4))
            finally:
                ablator.remove()
            delta = abl_loss - baseline_loss
            row = {
                "fraction": frac,
                "seed": seed,
                "n_units_ablated": k,
                "selection_hash": sel_hash,
                "ablated_loss": abl_loss,
                "delta": delta,
                "delta_over_noise": delta / noise_threshold,
                "wall_seconds": round(time.time() - t0, 2),
                "box": box_load(),
            }
            results.append(row)
            print(json.dumps({k2: v for k2, v in row.items() if k2 != "box"}), flush=True)

    report["ablation"] = results

    # ---------------- verdict proposal ----------------
    by_frac = {}
    for frac in FRACTIONS:
        ds_ = [r["delta"] for r in results if r["fraction"] == frac]
        ok = all(d > noise_threshold for d in ds_)
        loose = all(d > 0 for d in ds_)
        by_frac[str(frac)] = {
            "deltas": ds_,
            "delta_mean": float(np.mean(ds_)),
            "seed_spread": float(max(ds_) - min(ds_)),
            "all_above_threshold": ok,
            "all_positive": loose,
        }
    if all(v["all_above_threshold"] for v in by_frac.values()):
        verdict = "proved"
    elif all(not v["all_positive"] for v in by_frac.values()):
        verdict = "disproved"
    else:
        verdict = "inconclusive_lean_proved" if all(v["all_positive"] for v in by_frac.values()) else "inconclusive_lean_disproved"
    report["summary"] = {"by_fraction": by_frac, "proposed_verdict": verdict}
    report["box"]["end"] = box_load()
    report["wall_seconds_total"] = round(time.time() - t_start, 2)

    with open(OUT_JSON, "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print(f"\nproposed verdict: {verdict}", flush=True)
    print(f"wrote {OUT_JSON}", flush=True)
    print(json.dumps(report["summary"], indent=2, default=str), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
