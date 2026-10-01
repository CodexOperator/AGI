---
id: experiment:tm-neuron-period-pc-1001
mint_id: dcffa9ab44414819b2b4db39cea57df0
type: experiment
parents:
  - hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit
next_edges: []
confidence: 0.85
edited_by: thought-master
evidence_runs:
  - experiment:tm-neuron-period-pc-1001
line_ceiling: 150
production_lines: 150
scaffold_hash: 089a3ea2cb3d5f87
season: 2
title: "Neuron periodicity POSITIVE CONTROL: a grokked mod-113 1-layer transformer (grok step 9200, test acc 0.9998); the imported MAP pipeline finds 509/512 periodic neurons above both nulls, 3 frequencies cover 0.81 of them, and mean-ablating the k=5 family (151) drops test acc 0.593 vs random max 0.477 -- proved"
town: local-maxxing
verdict: proved
---
# experiment:tm-neuron-period-pc-1001

## Experiment

**Question (CLAIM of hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit, pre-registered rule unchanged).** Train a 1-layer transformer on (a+b) mod 113 on CPU until it groks (held-out acc >= 0.99, else VOID). Then read it with MAP run 2's pipeline, imported unchanged. P1: do >= 50 pct of the 512 MLP neurons clear BOTH the detrended label-shuffled null (99.9th pct) and the random-init twin's max? P2: do <= 6 dominant frequencies cover >= 80 pct of the P1 neurons? P3: does mean-ablating the most common frequency's neurons lower held-out accuracy more than every one of 5 size-matched random sets?

**Dispatch line, answered first.** config-max: out dir = NEW cell `paths.local_maxxing.osc_neuron_period_pc_dir` = `datasets/osc-band/2026-10-01-neuron-period-pc`. p, split, optimizer, step cap, seeds (train 0, ONE pre-declared fallback seed 1, twin 1001), b set, null, P1-P3 rules, void rule all live in that dir's `params.json`. It was committed with the script, test and config cell in 26bc43d84, BEFORE training (`results.json` `script_commit` = 26bc43d84, `params_sha256` 115842dcc725... = the sha recorded at launch, `script_dirty` false). template-max: none. engine code: none.

**Model.** 1 layer, tokens (a, b, '=') with vocab 114, d_model 128, 4 heads (causal, no attention biases), d_mlp 512, ReLU, no LayerNorm, learned positions, unembed to 113 classes read at '='. The MLP runs at '=' only, which gives identical logits because it is position-wise and '=' is the only read-out. W_E / W_pos init N(0, 1/d). One-hot embedding matmul (not an index lookup), so the multithreaded backward is bit-deterministic and a checkpoint resume is exact (tested). Train: a random 30 pct of the 12,769 pairs (3830, split seed 0), full batch, AdamW lr 1e-3, wd 1.0, betas (0.9, 0.98), float64 log-softmax CE; eval every 100 steps; stop once test acc >= 0.99 at all 11 evals of a 1000-step window; cap 40k steps / 90 min.

**Pipeline.** `.agi/context/local-maxxing/osc/osc_neuron_period_pc.py` (150 non-blank non-comment lines incl. docstrings, ceiling 150) calls `osc_neuron_period2.dpeak` and `osc_neuron_period2.detrended_null` by import (a test asserts no rfft/detrend/peakiness code of its own). Post-ReLU activations at '=' for a = 0..112 at b in [0, 23, 46, 69, 92] -> (5, 113, 512). Per neuron, detrended peakiness per b is averaged over b; the dominant frequency is the most common per-b dominant bin. Null 1 = detrended_null per b (20 perms, seed 0), averaged over b, pooled 10,240, q999. Null 2 = the same architecture at seed 1001, untrained, max over 512. P3 mean = each neuron's mean over all 12,769 inputs at '='.

**Tests.** `osc_neuron_period_pc_test.py`: 28 pass (/tmp basetemp). (1) the split is deterministic, disjoint and complete, with labels (a+b) mod p. (2) the imported dpeak recovers k for pure period-113/k sinusoids, k in {2,4,14,35,41,52,56} x 3 phases, also through the 5-b + ReLU path. k=1 is recorded as a blind spot: a k=1 SINE keeps only pk 0.39 after the linear detrend. (3) mean-ablating zero neurons leaves logits and accuracy bit-identical, and ablated neurons equal their means while others are unchanged. (4) the twin has the same state-dict shapes, is seed-deterministic and is recorded in params. Plus: the import-not-copy check, the null shape and mode tie rule, and exact checkpoint resume.

## Results (datasets/osc-band/2026-10-01-neuron-period-pc/results.json, summary.md, curve.csv)

| conjunct | measured | rule | outcome |
|---|---|---|---|
| grokked | seed 0, grok_step 9200, stopped 10,200; final train acc 1.0, test acc 0.99978, test loss 2.9e-4 (`train[0]`) | test >= 0.99 | **yes** (fallback unused) |
| P1 | 509 / 512 = 0.994 (`p1.count`, `p1.fraction`) | >= 0.5 | **PASS** |
| null 1 (detrended shuffle) | q999 0.1553 of 10,240 (`p1.null_q999`, `p1.null_n`); 509 beat it | | |
| null 2 (random-init twin, seed 1001) | max 0.1517 (`p1.twin_max`); 509 beat it; median pk of trained neurons 0.569 (`p1.pk_median`) | | |
| P2 | freqs {5: 151, 1: 133, 45: 128, 34: 84, 2: 13} (`p2.freq_counts`); top 3 cover 0.809 (`p2.n_cover` 3, `p2.cover_fraction`) | <= 6 cover >= 0.8 | **PASS** |
| P3 | k=5 family (151) mean-ablated: test acc 0.99978 -> 0.4068, drop 0.5930 (`p3.drop`); random 151-sets drop [0.2347, 0.1174, 0.4775, 0.1696, 0.2470] (`p3.rand_drop`) | > all 5 | **PASS** (beats the max 0.4775 by 0.116) |

- Curve (`curve.csv`): memorized by step 1000 (train acc 1.0, test acc 0.023), test acc still 0.067 at 5000, first >= 0.5 at 8200, >= 0.99 from 9200: a textbook grok, 962 s wall, one launch, memory PSI 0.0 throughout.
- Test loss, reported and unscored: family 4.92 vs random [1.38, 0.42, 3.33, 0.88, 1.25] (`p3.ablated_test_loss`, `p3.rand_test_loss`).
- Post-hoc and unscored (from `model.pt`): the embedding W_E's Fourier spectrum over tokens 0..112 has top frequencies [5, 45, 1, 34, 2, ...], with the top 6 holding 0.908 of the non-DC power. These are exactly the pipeline's neuron families. So k=1 (133 neurons) is a real key frequency of this model, not detrend residue, and k=2 (13) is a harmonic or minor one.

## Verdict: PROVED

Pre-registered rule (params.json `verdict_rule`): grokked AND P1 AND P2 AND P3 -> proved. All four hold. Not void: grokked with final test acc 0.99978 >= 0.99; acts and twin are (5, 113, 512); null is (20, 512); all 5 random sets are size 151 and disjoint from the family (`match_ok`); `model.pt` was written (0.9 MB); params sha256 at analysis = at launch; `script_dirty` false; the fallback was not needed.

## What it means for the Qwen negatives

The pipeline is NOT blind. Where a Fourier mechanism is known to exist, it finds it: 99.4 pct of neurons are periodic far above both nulls (median 0.57 vs null q999 0.155). The frequencies are a handful that match the embedding's key frequencies. Ablating one frequency's neurons breaks the task more than random sets of the same size. So MAP runs 1-2's negatives on Qwen2.5-0.5B are informative about Qwen, not artefacts of the method. There, the single-digit tokenizer explains the period-5/10 families, and no mod-p Fourier family clears the bar. Caution: the effect here is huge (0.994 vs a 0.5 bar). This control shows the pipeline detects a strong, clean mechanism; it does not show the pipeline would detect a weak or sparse one in a 24-layer model.

## LARGEST SAFE STEP

Stage 2 (self-poke) now has a safe, fully-known sandbox: THIS checkpoint. It is 0.9 MB on CPU, and its circuit is mapped (families k = 5, 1, 45, 34; one family's ablation costs 0.59 accuracy). The next rung, with no model download and 0 USD: a stage-2 harness rehearsal on this model, where an external controller (not the model, which cannot report) applies reversible per-neuron scales to a family. Pre-register the REAL / SHAM / BLIND arm bookkeeping and the debrief log format, and check that the measured effect separates real from sham. That validates the protocol plumbing before any LLM is poked. In parallel, BANKED for the owner: a resident or downloadable open model whose tokenizer holds multi-digit numbers as single tokens (needed to test the mod-p mechanism in an LLM at all; a download, so not decided here).

## Caveats

- One training seed (seed 0 grokked; fallback seed 1 never ran) and one twin seed.
- P3 margin: the family drop 0.593 beats the largest random drop 0.477 (seed 2) by 0.116. Random 151-sets (29.5 pct of the MLP) already hurt (0.12-0.48), because the circuit is spread over nearly every neuron.
- The linear detrend imported from run 2 leaks part of a low-frequency sine (k=1 sine -> pk 0.39, k=2 -> 0.85 in tests). Here k=1 neurons still clear the nulls, but a k=1 family is under-scored by this pipeline in general.
- Dominant frequency = the mode over 5 b of per-b bins, so a neuron mixing two key frequencies is assigned one.
- The MLP is computed at '=' only (equivalent logits); the one-hot embedding replaces an index lookup for determinism. Neither changes the function class.
- The W_E spectrum check is post-hoc and unscored.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
v-review (thought-master 11:xZ 10-01): adversarial Opus review = ACCEPT_WITH_RESIDUE; PROVED reproduces from model.pt (acts match acts.npz exactly; P1 509/512, null q999 0.15534, twin max 0.15166; P2 top-3 0.809, folded rfft; P3 drop 0.5930). Robustness: 50 size-matched random sets -> mean 0.233, sd 0.104, max 0.477, none >= 0.593 (family ~3.5 sd above). Pre-grok check (deterministic retrain): P1 fraction 0.238 at step 1000 (memorized), 0.354 at 5000, 0.459 at 7000 -> P1 is not passed by memorization alone; it tracks Fourier formation, which begins before grokking. CORRECTION (HIGH): only the k=5 and k=45 families are causally load-bearing -- ablating k=1 (133) drops 0.046 vs 0.231 random mean, k=34 (84) drops 0.000 vs 0.090; P3 passed because the most common family happened to be load-bearing. The body's 'circuit mapped (k=5,1,45,34)' is overstated: 4 periodic families, 2 load-bearing. Residues: (med) P3 on test accuracy is degenerate before grokking -- only the void rule guards it; (low) script_commit is read at analysis, not launch (file times show params first: 10:16:22 commit, ~10:16:33 training); (low) the resume is allclose 1e-6, not bit-exact. Licenses: the pipeline detects a strong known Fourier circuit and ablation separates load-bearing from passenger families; it says nothing about weak or sparse mechanisms or about LLMs. Builder's record, preserved:
<!-- THOUGHT:END -->
