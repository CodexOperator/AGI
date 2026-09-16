#!/usr/bin/env python3
"""D1 conjunct-2 DIAGNOSTIC: why does drop_low lose to drop_rand?

d1_predictiveness.py measured, at the same 5% byte budget:
    drop_low  delta = +0.394   (signal's recommendation)
    drop_rand delta = +0.205   (no information; seeds 0/1/2)
    drop_high delta = +7.923   (positive control)
i.e. the globally-lowest-proxy units HURT MORE than a random subset while the
SINGLE-UNIT probes showed a positive rank signal (spearman 0.779). That is only
consistent if the low-proxy selection is biased in a way the per-unit proxy
does not see. The obvious candidate: mean activation magnitude grows with
depth, so ranking GLOBALLY by mean_abs*col_norm concentrates the "lowest" units
in the earliest layers -- the selection ends up removing ~5% of the whole model
but a much larger fraction of a few layers.

This script measures the mechanism and runs the fair control:
  * layer histogram of the low / high / random 5% selections,
  * drop_low_balanced -- the same number of lowest-proxy units PER LAYER, so
    every layer loses the same 5%. If the signal is real once the layer
    confound is removed, loss(drop_low_balanced) < loss(drop_rand).

Usage: ~/.venv-lm/bin/python .agi/context/local-maxxing/d1/d1_predictiveness_diag.py
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time

import numpy as np
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import d1_ablation as A        # noqa: E402
import d1_predictiveness as P  # noqa: E402

OUT_JSON = os.path.join(HERE, "d1_predictiveness_diag_results.json")
FRACTION = 0.05
RAND_SEED = 0


def main() -> int:
    t_start = time.time()
    report = {"script": os.path.abspath(__file__), "fraction": FRACTION,
              "box": {"start": A.box_load()}}
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(A.MODEL_ID)
    try:
        model = AutoModelForCausalLM.from_pretrained(A.MODEL_ID, dtype=torch.float32)
    except TypeError:
        model = AutoModelForCausalLM.from_pretrained(A.MODEL_ID, torch_dtype=torch.float32)
    model.eval()
    down_projs = A.find_down_projs(model)
    per_layer = down_projs[0][1].in_features
    n_layers = len(down_projs)
    total = per_layer * n_layers
    k = int(round(FRACTION * total))

    from datasets import load_dataset
    ds = load_dataset(A.EVAL_DATASET, A.EVAL_CONFIG, split=A.EVAL_SPLIT)
    text = "\n\n".join(t for t in ds["text"] if t.strip())
    ids = tok(text, return_tensors="pt").input_ids[0][:A.N_WINDOWS * A.WINDOW]
    assert hashlib.sha256(ids.numpy().tobytes()).hexdigest()[:16] == "cafa6c30c6d28f7d"
    windows = [ids[i * A.WINDOW:(i + 1) * A.WINDOW].unsqueeze(0) for i in range(A.N_WINDOWS)]
    batch4 = [torch.cat(windows[i:i + 4], dim=0) for i in range(0, A.N_WINDOWS, 4)]

    # proxy (identical to d1_predictiveness.py)
    sums = [torch.zeros(per_layer, dtype=torch.float64) for _ in down_projs]
    counts = [0]

    def mk(i):
        def hook(module, args):
            x = args[0]
            sums[i] += x.detach().reshape(-1, x.shape[-1]).abs().sum(dim=0, dtype=torch.float64)
            if i == 0:
                counts[0] += x.shape[0] * x.shape[1]
        return hook

    hs = [m.register_forward_pre_hook(mk(i)) for i, (_, m) in enumerate(down_projs)]
    try:
        A.forward_loss(model, [torch.cat(windows, dim=0)])
    finally:
        for h in hs:
            h.remove()
    mean_abs = torch.cat([(s / counts[0]).to(torch.float32) for s in sums])
    col_norm = torch.cat([m.weight.detach().float().norm(dim=0) for _, m in down_projs])
    proxy = (mean_abs * col_norm).detach().numpy()

    order = np.argsort(proxy)
    low = order[:k]
    high = order[-k:]
    rng = np.random.default_rng(RAND_SEED)
    rand = np.sort(rng.choice(total, size=k, replace=False))

    def layer_hist(units):
        return np.bincount(units // per_layer, minlength=n_layers).tolist()

    report["layer_histograms"] = {
        "low": layer_hist(low), "high": layer_hist(high), "rand": layer_hist(rand),
        "per_layer_mean_of_mean_abs": [
            float(mean_abs[i * per_layer:(i + 1) * per_layer].mean()) for i in range(n_layers)],
    }
    # layer-balanced low: k//n_layers per layer
    per = k // n_layers
    balanced = []
    for i in range(n_layers):
        layer_units = order[i * per_layer:(i + 1) * per_layer]
        balanced.extend(layer_units[:per].tolist())
    balanced = np.array(sorted(balanced))
    report["balanced_n_units"] = int(len(balanced))
    report["layer_histograms"]["low_balanced"] = layer_hist(balanced)

    dropper = P.UnitDropper(model, n_layers)
    base = A.forward_loss(model, batch4)
    results = []
    for name, units in (("drop_low_balanced", balanced),):
        t0 = time.time()
        dropper.drop(units.tolist(), per_layer)
        try:
            loss = A.forward_loss(model, batch4)
        finally:
            dropper.restore()
        row = {"condition": name, "n_units": len(units), "loss": loss,
               "delta": loss - base, "wall_seconds": round(time.time() - t0, 2)}
        results.append(row)
        print(json.dumps(row), flush=True)
    report["baseline_loss"] = base
    report["results"] = results
    report["wall_seconds_total"] = round(time.time() - t_start, 2)
    report["box"]["end"] = A.box_load()
    with open(OUT_JSON, "w") as fh:
        json.dump(report, fh, indent=2, default=str)
    print("wrote", OUT_JSON, flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
