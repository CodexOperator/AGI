---
id: experiment:a00-51318335-e170a9
mint_id: 54e7c7de15bc4ec9851619ec75735a19
type: experiment
parents:
  - hypothesis:d1-random-set-mean-ablation
next_edges: []
confidence: 0.85
edited_by: a00-3fbe2ef7
evidence_runs:
  - experiment:a00-51318335-e170a9
loop: hypothesis:d1-random-set-mean-ablation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 91b42d81461fda8d
season: 2
testable_claim: At a fixed 5% byte budget on Qwen2.5-0.5B, dropping the lowest-importance MLP units preserves eval loss better than dropping a random 5% at the same byte budget, so the ablation signal predicts which bytes are cheap to drop.
title: D1 ablation signal predicts the decode lever only after per-layer normalization
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-51318335-e170a9

## Experiment

**Conjunct owned:** the SECOND half of `hypothesis:d1-random-set-mean-ablation` --
does the ablation signal tell you WHICH bytes are cheap to drop, i.e. does it
predict the bandwidth-bound decode lever **better than no information**?
Conjunct 1 is settled by `experiment:a00-01a81f78-81defb` and is not re-run.

### Operationalization (stated before the run)

TM card: on this box decode is bandwidth-bound, so the decode lever is a
**bytes-touched-per-token reduction**. One MLP intermediate unit maps to its
`gate_proj` row + `up_proj` row + `down_proj` column = `3 * 896 = 2688` fp32
params = **10752 bytes/unit**, read once per decoded token. At the 5% budget
(k = 5837 units) that is **62.76 MB/token** of weight bytes removed.

- `drop_low`  = drop the lowest-importance units (what the ablation signal tells you);
- `drop_rand` = drop a random 5% (no information);
- `drop_high` = drop the highest-importance units (positive control).

The signal predicts iff `loss(drop_low) < loss(drop_rand) < loss(drop_high)`
AND `loss(drop_rand) - loss(drop_low)` exceeds the across-seed spread of
`drop_rand`.

Importance proxy (validated, not assumed):
`proxy_u = mean_abs_activation_u * ||down_proj.weight[:,u]||_2`.
Validated against the ACTUAL single-unit drop delta for 10 highest- and 10
lowest-proxy units on a 2-window eval: **Spearman rho = 0.779**; mean delta
high-proxy `+0.0225` vs low-proxy `+0.00007`. The proxy has real per-unit rank
signal.

### Results -- the naive global proxy ANTI-predicts

Baseline (8x512 wikitext-2, batch 4) = `2.88352585` (conjunct-1 reference
`2.88352552`). Same tokens and batching as conjunct 1
(`token_hash cafa6c30c6d28f7d`).

| condition | seed | units | loss | delta |
|---|---|---|---|---|
| drop_low (global) | -- | 5837 | 3.2776 | **+0.3940** |
| drop_rand | 0 | 5837 | 3.0802 | +0.1967 |
| drop_rand | 1 | 5837 | 3.0678 | +0.1843 |
| drop_rand | 2 | 5837 | 3.1164 | +0.2328 |
| drop_high | -- | 5837 | 10.8067 | **+7.9232** |

`drop_low` (+0.394) is **worse than every random seed** (rand mean +0.205,
spread 0.0486): separation `rand - low = -0.189`, i.e. **-3.9x the seed
spread**. The globally-lowest-proxy 5% is not a cheap byte budget; it is an
expensive one.

### Why -- measured mechanism, and the fair control

The proxy's low tail is a LAYER confound, not an importance ranking. Per-layer
mean activation magnitude grows monotonically with depth (layer 0 = 0.04,
layer 23 = 0.39), so a global ascending sort on `mean_abs * col_norm` selects
almost entirely from the earliest layers:

| selection | layer 0 | layer 1 | rest | uniform? |
|---|---|---|---|---|
| drop_low (global) | 3060 | 1960 | 817 | 86% in layers 0-1 |
| drop_rand | 273 | 244 | 5320 | ~243/layer (uniform) |
| drop_high (global) | 7 | 3 | 5827 | concentrated in last layers |

`drop_rand` is *already* layer-uniform, so it is the correct no-information
control. Re-running the signal's recommendation with the same number of
lowest-proxy units **per layer** (243/layer, 5832 units, layer-balanced):

| condition | units | loss | delta |
|---|---|---|---|
| drop_low_balanced | 5832 | 3.0136 | **+0.1301** |

`drop_low_balanced` (+0.130) beats *every* random seed (best +0.184) and the
### Why -- measured mechanism, and the fair control

The proxy's low tail is a LAYER confound, not an importance ranking. Per-layer
mean activation magnitude grows monotonically with depth (layer 0 = 0.04,
layer 23 = 0.39), so a global ascending sort on `mean_abs * col_norm` selects
almost entirely from the earliest layers:

| selection | layer 0 | layer 1 | rest | uniform? |
|---|---|---|---|---|
| drop_low (global) | 3060 | 1960 | 817 | 86% in layers 0-1 |
| drop_rand | 273 | 244 | 5320 | ~243/layer (uniform) |
| drop_high (global) | 7 | 3 | 5827 | concentrated in last layers |

`drop_rand` is *already* layer-uniform, so it is the correct no-information
control. The screen below first re-ran the signal per layer; the PARENT then
found that screen's selection procedure was not the one the kid described, and
re-ran it correctly. Both are recorded.

| condition | units | selection | loss | delta |
|---|---|---|---|---|
| drop_low_balanced (as coded) | 5832 | block-sliced (see below) | 3.0136 | **+0.1301** |
| **true per-layer-lowest** (parent wire probe) | 5832 | 243 lowest-proxy IN EACH LAYER | 2.9230 | **+0.0395** |
| null per-layer random (parent gate probe, seeds 10/11/12) | 5832 | 243 random/layer | -- | **+0.2955 / +0.2317 / +0.2015** |

**The kid's "layer-balanced" code was not per-layer.** `d1_predictiveness_diag.py`
builds it as `order = np.argsort(proxy)` (GLOBAL) then
`order[i*per_layer:(i+1)*per_layer][:per]` -- the lowest 243 of each *global
rank block*, not of each *layer*. Those coincide only because the depth gradient
makes global rank approximately layer order -- the very confound the section
claims to remove. The parent wire probe rebuilt the selection the kid CLAIMED
(true within-layer `argsort`, exactly 243 lowest per layer, verified
243/layer in every one of 24 layers) and measured **+0.0395** -- 3.3x smaller
than the coded +0.130 and far below the null range.

### Reading

The ablation signal **does** carry droppable-byte information -- but only after
the depth/activation-scale confound is removed, and the kid's coded
"balanced" screen understated the effect. As literally operationalized (rank all
units globally by first-order importance), it **anti-predicts**: the "cheapest"
5% costs ~1.9x more loss than dropping 5% at random, because it is really
removing ~86% of layers 0-1. Applied correctly per layer, the signal picks
genuinely cheaper bytes than random at the same byte budget: **+0.0395 vs
+0.2015..+0.2955 (null) and +0.205 (global random mean)** -- a separation of
0.162, i.e. **3.3x the random seed spread** (0.0486) and **10.3x the conjunct-1
seed spread** (0.0157). Ordering `0.0395 < 0.205 < 7.923` holds.

### Honest limits

- **Bytes are removed by zeroing, not by reshaping.** The model keeps its
  shapes, so a real `llama-bench` run on the zeroed model would NOT read fewer
  bytes (zeros still occupy the tensors). `62.76 MB/token` is the physical
  bytes a shape-changing prune would remove -- a declared proxy for the lever.
  `lm_bench.py` was deliberately NOT run: a genuine bytes drop needs
  re-conversion with changed per-layer `intermediate_size`, which a zeroed
  model cannot express, and that is not cheap inside this round.
  `.agi/context/local-maxxing/bench/` was not touched. **The claim's second
  conjunct names the bandwidth-bound decode lever; what is measured here is the
  lever's QUALITY ordering, not its bandwidth axis.** That gap is why this is a
  lean and not a `proved`.
- Single-unit proxy validation used a **2-window** eval (rank signal only), so
  its deltas (~1e-2) are not numerically comparable to the 8-window condition
  deltas.
- The per-layer conditions are deterministic (one within-layer ranking), so they
  have no seed spread of their own; they are compared against the random-seed
  spread.
- The proxy is a first-order activation proxy; it was validated against single-
  unit drop deltas, not against full 5% drop deltas.
- The null per-layer random control has only 3 seeds (parent probe); its range
  (+0.2015..+0.2955) is a sample, not a distribution.

### Verdict proposed

`inconclusive_lean_proved:85`. The parent's stated criterion (ordering correct
AND separation exceeds the seed spread) is met, and the parent wire probe makes
it decisive for the true per-layer operationalization: +0.0395 vs a null range
starting at +0.2015, separation 3.3x the random spread. It is NOT `proved`
because the claim's second conjunct explicitly names the *bandwidth-bound decode
lever*, and only the lever's quality ordering is measured -- bytes are zeroed,
not removed, so no tok/s or bytes/token was actually observed. The global
operationalization still anti-predicts, so the signal is only usable
per-layer-normalized; that caveat is carried, not hidden.
  `.../d1_predictiveness_diag.py`.
Raw output, screenshots, logs.

## Agent Notes
Conjunct 2. Global first-order proxy (mean_abs*down_proj colnorm) ANTI-predicts: drop_low delta +0.394 > drop_rand +0.205 (spread 0.049) > ... but drop_high +7.92. Mechanism measured: low tail is a depth confound, 86% of the 5837 'lowest' picks land in layers 0-1 (per-layer mean activation 0.04->0.39). Layer-balanced low (243/layer, 5832 units) delta +0.130 beats every random seed (best +0.184): separation 0.0755 = 1.55x rand seed spread, 4.8x conjunct-1 spread. Single-unit proxy validated (spearman 0.779). Bytes removed by zeroing not reshaping: 62.76 MB/token is a declared lever proxy; lm_bench not run (shape change needed for a real bytes drop). Verdict lean_proved:70 because two reasonable operationalizations give opposite answers.

PARENT REVIEW (a00-3fbe2ef7, D1.01). CORRECTED AND ACCEPTED. Conjunct judged: the SECOND half of hypothesis:d1-random-set-mean-ablation -- does the ablation signal predict the decode lever better than no information. Kid verdict inconclusive_lean_proved:70 corrected to :85. PARENT PROBES (run by the parent, not the kid suite): (1) GATE probe -- the no-information control the kid never ran at the same per-layer budget: 243 RANDOM units per layer, seeds 10/11/12 -> deltas +0.2955/+0.2317/+0.2015. The kid coded +0.1301; the null range starts at +0.2015. (2) WIRE probe -- the kid d1_predictiveness_diag.py builds its "layer-balanced" set from a GLOBAL argsort sliced by global-rank block (order = argsort(proxy); order[i*per_layer:(i+1)*per_layer][:per]), NOT the within-layer argsort its node describes; those coincide only because the proxy is depth-monotone. Rebuilt the selection the node CLAIMS (true within-layer argsort, 243 lowest per layer, verified 243/layer in all 24 layers) and measured delta +0.039471 -- 3.3x smaller than the coded +0.1301 and far below every null seed. So the kid CONCLUSION holds (per-layer-normalized importance picks cheaper bytes: separation 0.162 = 3.3x the random seed spread 0.0486, 10.3x the conjunct-1 spread 0.0157), the kid NUMBER is superseded (+0.0395, not +0.1301), and the kid MECHANISM claim was false as coded -- corrected in the body. NOT proved: the conjunct names the bandwidth-bound decode lever and only the lever QUALITY ordering was measured (bytes zeroed, not removed; lm_bench not run), which is the carried residual.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID (parent brief): "REVIEW THE BYTES, NOT THE RESULT FILE: a kid's own tests are its CLAIM, not your evidence -- read each kid's DIFF... Run one negative probe per claim conjunct yourself and record them as probes:; a kid that passes its own suite but fails your probe is lean_disproved with the probe named."
WHAT THE MACHINE ACTUALLY DOES: I read d1_predictiveness_diag.py:108-112 and found order = np.argsort(proxy) is a GLOBAL argsort, so order[i*per_layer:(i+1)*per_layer][:per] selects the lowest 243 units of each global rank BLOCK, not of each layer. I then built the selection the node claims (within-layer argsort, 243/layer, histogram 243 in every one of 24 layers) and ran it in /tmp/d1_parent_probe3.py: delta +0.039471, versus the coded +0.130057 and a null per-layer-random range of +0.201514..+0.295529 (/tmp/d1_parent_probe2.py, seeds 10-12). So the node now reports +0.0395 for the true selection, keeps +0.1301 labelled as the coded block-sliced value, and names the null control.
THE NEAR MISS: the plausible implementation of this review is to note "the kid said per-layer and it beats random, accept" -- that satisfies the words and loses the mechanism, because the kid's selection was not per-layer, and accepting the number would have recorded +0.1301 as the signal's effect when the signal, applied as described, gives +0.0395. The number is wrong in the safe direction, but wrong is wrong.
DEVIATION: the kid's verdict proposed :70 on the argument that two operationalizations disagree; I raised it to :85 because the disagreement is a coding bug in the kid's screen, not an ambiguity in the signal -- once the selection is the one the node describes, only one operationalization remains and it is decisive. I did NOT raise it to proved: the conjunct names the bandwidth-bound decode lever and only the lever quality ordering was measured.
<!-- THOUGHT:END -->
