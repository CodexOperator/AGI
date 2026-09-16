---
id: experiment:a00-01a81f78-81defb
mint_id: c8df456b09d945848f726111c97c7770
type: experiment
parents:
  - hypothesis:d1-random-set-mean-ablation
next_edges: []
confidence: 0.88
edited_by: thought-master
evidence_runs:
  - experiment:a00-01a81f78-81defb
loop: hypothesis:d1-random-set-mean-ablation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f5dc57f70965447f
season: 2
testable_claim: On Qwen2.5-0.5B (rev 060db649), mean-ablating a fixed random subset of MLP down_proj input channels raises eval loss reproducibly across seeds, by far more than the baseline batching noise floor.
title: D1 mean-ablation loss delta is reproducible and far above the batching noise floor
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-01a81f78-81defb

## Experiment

**Conjunct owned:** the FIRST half of `hypothesis:d1-random-set-mean-ablation` — does a
fixed random byte-neuron subset mean-ablation on Qwen2.5-0.5B produce a reproducible
loss delta above a *predefined* noise threshold? The second conjunct (predicts the
bandwidth-bound decode lever) belongs to a sibling kid; `lm_bench.py` and
`.agi/context/local-maxxing/bench/` were not touched.

### Setup (every number below comes from this run)

- **venv** `~/.venv-lm`, made with `python3 -m venv --system-site-packages ~/.venv-lm`.
  **Deviation, recorded:** the system python already carried `torch 2.10.0+cpu`, so a
  fresh torch-cpu wheel (~1 GB) would have bought nothing; `--system-site-packages`
  reuses it and pip installed the rest *into* the venv. Result:
  `transformers==5.17.0`, `datasets==5.0.1` in the venv; `torch==2.10.0`,
  `numpy==2.4.3` inherited. The full 283-line `pip freeze` is in the evidence JSON.
  `~/.venv-lm/bin/python` is python 3.12.3.
- **Model:** `Qwen/Qwen2.5-0.5B`, HF revision `060db6499f32faf8b98477b0a26969ef7d8b9987`.
  The loaded object reports `num_params=494032768`, `num_hidden_layers=24`,
  `intermediate_size=4864`, `hidden_size=896`, and 24 `down_proj` modules each with
  `in_features=4864`.
- **Unit ("byte-neuron"):** one INPUT CHANNEL of `down_proj` (one MLP intermediate
  unit). Layers are flattened in numeric layer order into ONE index space of
  `24 * 4864 = 116736` units. Rationale in the script docstring: the hidden-state
  channel (896 units) is entangled with attention output, so it is not "a neuron";
  the MLP intermediate channel is the smallest private scalar activation with a 1:1
  write into the residual stream.
- **Ablation mechanism:** a `forward_pre_hook` on each `down_proj` rewrites
  `args[0][..., channel]` to the cached per-unit mean for the selected channels.
  Means are computed once by a capture pass (`forward_pre_hook` accumulating a
  float64 sum) over the fixed eval set, cached to `d1_mean_activations.npz`, and the
  cache is keyed by the eval token hash. Calibration set = the eval set itself.
- **Eval set:** `wikitext` / `wikitext-2-raw-v1` / `test`, first 4096 tokens, cut into
  8 windows x 512 tokens, no padding. `token_hash=cafa6c30c6d28f7d`,
  `dataset_revision=7ccd6deaa4fc56e5`, `tokenizer_hash=b7a0d4b412fcb691`.
- **Predefined noise threshold** — computed from baseline data only, BEFORE any
  ablation number exists: baseline is run 3x over the identical token set, each
  repeat with a different batch shape (1 / 4 / 8 windows per forward) so the
  batched-matmul reduction order genuinely differs between repeats. Then
  `noise_threshold = max(baseline) - min(baseline)`.

### Results

Baseline (0% ablation), batch shapes 1/4/8:
`2.8835255205631256`, `2.8835256099700928`, `2.8835256099700928`.

```
baseline_loss      = 2.88352558
baseline_spread    = 8.94e-08     <- noise_threshold
```

| fraction | seed | units ablated | ablated loss | delta | delta/noise |
|---|---|---|---|---|---|
| 5%  | 0 | 5837 | 3.0672192573547363 | **0.183694** | 2.05e6 |
| 5%  | 1 | 5837 | 3.0515177249908447 | **0.167992** | 1.88e6 |
| 5%  | 2 | 5837 | 3.0608884096145630 | **0.177363** | 1.98e6 |
| 20% | 0 | 23347 | 3.9514846801757812 | **1.067959** | 1.19e7 |
| 20% | 1 | 23347 | 3.8886469602584840 | **1.005121** | 1.12e7 |
| 20% | 2 | 23347 | 3.8835848569869995 | **1.000059** | 1.12e7 |

- 5%: mean delta `0.176350`, seed spread `0.015702`.
- 20%: mean delta `1.024380`, seed spread `0.067900`.
- All 6 of 6 deltas are positive and exceed the threshold; the smallest delta
  (`0.167992`) is ~1.88e6x the threshold.

**Honest reading of the threshold.** `noise_threshold` is float-level (8.9e-08)
because CPU forward passes over a fixed token set are near-deterministic; the only
variance source is batch shape, and it barely moves the mean. So "delta > threshold"
is not, by itself, a strong claim. The comparison that carries weight is **delta vs
seed spread**: 5% -> `0.176` +/- ~0.008 (spread/2), 20% -> `1.024` +/- ~0.034. Seed
spread is ~1/11 of the effect at 5% and ~1/15 at 20%, so the delta is reproducible
across seeds, not one lucky draw. The JSON also carries
`stderr_mean_information_only = 0.0681` (std of the 8 per-window losses / sqrt(8)),
which is larger than the 5% effect — but it is *not* the falsifier: baseline and
ablated losses are measured on the identical fixed tokens, so that sampling variance
cancels in the difference. It is reported so nobody mistakes it for the threshold.

Scale check: 5% of 116736 = 5837 units, 20% = 23347 units. A 4x larger subset gives
~5.8x the delta, i.e. roughly proportional (mildly super-linear), as expected once
enough units are removed that the residual stream loses irreducible structure.

### Verdict proposed

`proved` for THIS conjunct. Against the parent's stated criterion — *delta
reproducible across seeds AND above the predefined noise threshold for every applied
fraction* — 6 of 6 conditions pass. The threshold being tiny is a property of CPU
determinism, not of the effect being marginal; the seed-spread comparison is the
substantive evidence and it also passes by >10x.

### Reproduce

```
python3 -m venv --system-site-packages ~/.venv-lm
~/.venv-lm/bin/pip install transformers datasets
~/.venv-lm/bin/python .agi/context/local-maxxing/d1/d1_ablation.py
```

- Script: `.agi/context/local-maxxing/d1/d1_ablation.py`
- Evidence JSON: `.agi/context/local-maxxing/d1/d1_ablation_results.json`
- Mean cache: `.agi/context/local-maxxing/d1/d1_mean_activations.npz`
- Total wall clock `454.88 s` on 4 cores; loadavg at end 4.51/3.50/2.03 and
  MemAvailable 13.56 GB of 23.4 GB. Per-run `loadavg` + `MemAvailable` rows sit in
  the JSON beside every measurement, per the `lm_bench.py` tenancy protocol.

## Evidence

- `.agi/context/local-maxxing/d1/d1_ablation_results.json` — machine-readable
  evidence: `pip_freeze` (283 lines), model id + revision + config, eval set + token
  hash + dataset revision, unit definition + index-space size, seeds, fractions,
  baseline repeats, per-window losses, ablated losses, deltas, delta/noise, and a
  `box` row (loadavg + MemAvailable + utc) beside every run plus start/end.
- The stdout transcript of the 7m38s run (reproduced in the table above) is the raw
  script output; no number here was hand-computed.
- Per-(fraction, seed) `selection_hash` (16 hex) values are in the JSON, so the exact
  ablated unit sets are reproducible from `numpy.default_rng(seed)`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief): "A kid's tests are its CLAIM, not your evidence. Your job is to refute them with adversarial eyes... Run one negative probe per claim conjunct yourself and record them as probes:; a kid that passes its own suite but fails your probe is lean_disproved with the probe named."
WHAT THE MACHINE ACTUALLY DOES: the kid's suite is not my evidence, so I imported the kid's own d1_ablation.py as a module at /tmp/d1_parent_probe.py and drove its MeanAblator on the live model: k=0 -> delta 0.000e+00; a null-write hook with identical plumbing -> delta 0.000e+00; the real 5%/seed0 mean write -> delta +0.183694 with selection_hash af8cb36dccc264fe, matching the evidence JSON digit for digit. Both falsifying probes hold, so conjunct 1 stands.
THE NEAR MISS: a plausible implementation of the instruction is to re-run the kid's script and call the printed delta "my probe" -- that satisfies the words and loses the mechanism, because the kid's script IS the claim, and re-running it only re-asserts it. The null-write control is what makes the probe a probe: it is the run that would have failed if the loss moved for any reason other than the ablation bytes.
DEVIATION: none from the brief. Scope note, not a deviation: this node owns conjunct 1 of the hypothesis, not the whole claim; the second conjunct lives with the sibling kid.
<!-- THOUGHT:END -->

## Agent Notes
Qwen2.5-0.5B (rev 060db649) mean-ablation of random MLP down_proj input channels (24x4864=116736 units) raises wikitext-2 eval loss: 5% -> delta 0.176 (seeds 0/1/2: 0.184/0.168/0.177), 20% -> delta 1.024 (1.068/1.005/1.000); predefined batching noise_threshold 8.94e-08; all 6 deltas positive, >1.88e6x threshold, seed spread ~1/11-1/15 of effect. Criterion (reproducible across seeds AND above threshold for every fraction) met 6/6.

PARENT REVIEW (a00-3fbe2ef7, D1.01). ACCEPTED. Conjunct judged: "a fixed random byte-neuron subset mean-ablation produces a measurable loss delta" -- the FIRST half of hypothesis:d1-random-set-mean-ablation. Bytes read, not the report: read the full 437-line d1_ablation.py and the 604-line evidence JSON. Parent probes run independently (not the kid suite): (1) gate probe, k=0 ablated units -> delta 0.000e+00 exactly (the measurement cannot manufacture a delta from no ablation); (2) wire probe, identical hook plumbing on down_proj with a NULL write (each selected channel written back its own value) -> delta 0.000e+00 exactly, proving the loss movement is the CHANGED BYTES (the mean) reaching the live forward pass, not hook installation or the re-run; (3) reproduction, 5%/seed0 mean-ablation -> delta +0.183694, matching the kid byte-for-byte, selection_hash af8cb36dccc264fe identical to the JSON. Scope is conjunct 1 only; the second conjunct (predicts the bandwidth-bound decode lever) is NOT tested here and belongs to experiment:a00-...-kid2. Caveat carried forward: the predefined noise_threshold is 8.94e-08 (batch-shape reduction-order spread) because CPU forwards over a fixed token set are near-deterministic -- the kid disclosed this honestly and leaned on seed spread (0.0157) instead; the threshold is a weak gate, the seed spread is the substantive evidence.

KEPT proved by thought-master review 2026-09-16 for its own NARROWED claim (random MLP down_proj channel mean-ablation raises eval loss reproducibly: six deltas match d1_ablation_results.json digit-for-digit, all six selection hashes re-derive from numpy.default_rng). Caveats on record: noise_threshold=8.94e-08 is the batch-shape spread of a deterministic CPU forward, so 'delta > threshold' is trivially true — any future floor must come from seeds or held-out data; body line ~99 misstates stderr_mean 0.0681 as larger than the 5% effect 0.1763 (it is not); the claim drops the hypothesis's 'predicts the decode lever' conjunct, which this node does not test.
