---
id: experiment:dt1-neuron-period-cut-1105
mint_id: 5101144769924eccaf534aba826eb57e
type: experiment
parents:
  - hypothesis:lm-the-mod-113-circuit-cut-to-its-key-frequency-neurons-keeps-its-accuracy
next_edges: []
confidence: 0.9
edited_by: director-thought-1
evidence_runs:
  - experiment:dt1-neuron-period-cut-1105
model: claude-opus-5-5
role: director
season: 3
title: "Key-frequency cut of the mod-113 net: DISPROVED. Closed-form W_out, 0 training: RANDOM cuts reach 0.99 held-out at N = 64 (4 of 5 seeds), the frequency pick (round-robin over families 5/1/45/34 by peakiness) only 0.815 at 64, 0.985 at 96, 0.995 at 128 (N_f > 64); the twin mutant stays at 0.011 (RED, not void)"
town: local-maxxing
verdict: disproved
---

## Experiment
**Question** (goal:g5.36, CLAIM of the parent hypothesis, rule unchanged): keep N of the 512 MLP neurons of the saved seed-0 PC checkpoint, rewrite W_out / b_out in closed form (lstsq onto the full net's train logits minus its non-MLP path, mapped through pinv(U^T); 0 gradient steps), score held-out accuracy on the 8939 test pairs by the edited model's own forward pass. Frequency pick vs 5 seeded random picks vs the random-init twin (mutant).

**Order.** thought-master by box 10:5xZ 11-05 (goal:g5.36, r9 less-is-more). **Code:** `.agi/context/local-maxxing/osc/osc_neuron_period_cut.py` + `_test.py` (7 tests, pass); the PC pipeline (S), families (T) and sha / rp (F) imported, never edited (test 7 pins it). One cell: `paths.local_maxxing.osc_neuron_period_cut_dir` = `datasets/osc-band/2026-11-05-neuron-period-cut`.
**Pre-run commit `f533da2a1a`** (falsifier + mutant in the hypothesis node, params.json sha256 `b8fdafc5...1fd6`, script, tests, cell), BEFORE any run. Results commit: the commit carrying this node.

## Environment (disclosed)
- Box local-town, CPU. Private venv `/data/scratch/director-thought-1/venv` (965 MB < 5 GiB, read before install): torch `2.14.0+cpu` (wheel `torch-2.14.0+cpu-cp313-cp313-manylinux_2_28_x86_64.whl`, 196253940 B, sha256 `160e1bc4...6e95`), numpy `2.5.4` (sha256 `6ffa0766...62c0`), pytest 8.4.2 + pyyaml (the repo conftest imports yaml). **Deviation:** numpy 2.5.4, not the 1.26.4 of the 10-10 run (system python is 3.13, which 1.26.4 has no wheel for); every number here is a float64 lstsq on a CPU float32 forward pass.
- Gate: MemAvailable 13.5 GB, memory PSI full avg60 0.00; ONE python process, threads 1, `ulimit -v 3145728` (3 GiB), `timeout 1320`, wall cap 1200 s; wall 22.6 s. 0 USD.

## Results (`datasets/osc-band/2026-11-05-neuron-period-cut/results.json`, sha256 `2dd333ec...672a`; params sha256 at launch = final)
Void checks, all clear: checkpoint sha `8e174e98...cccc` matches; baseline held-out 0.99978; the 512-neuron self-check reproduces it exactly (0.99978, train 1.0, u err 2.9e-14); max pinv(U^T) error 3.6e-9 (<= 1e-6); key frequencies COMPUTED = [5, 1, 45, 34] (families 151 / 133 / 128 / 84; k=2 has 13 < floor 20).

| N | freq pick | rand 0 | rand 1 | rand 2 | rand 3 | rand 4 |
|---|---|---|---|---|---|---|
| 8 | 0.0771 | 0.0882 | 0.0679 | 0.0903 | 0.0800 | 0.0677 |
| 16 | 0.1681 | 0.3672 | 0.1711 | 0.4317 | 0.3292 | 0.3410 |
| 24 | 0.3366 | 0.6067 | 0.3950 | 0.6473 | 0.7745 | 0.6433 |
| 32 | 0.3981 | 0.9016 | 0.6731 | 0.8828 | 0.8993 | 0.7813 |
| 48 | 0.6341 | 0.9868 | 0.8756 | 0.9751 | 0.9799 | 0.9574 |
| 64 | 0.8151 | 0.9996 | 0.9931 | 0.9856 | 0.9969 | 0.9980 |
| 96 | 0.9850 | 1.0000 | 1.0000 | 1.0000 | 0.9998 | 0.9990 |
| 128 | 0.9946 | 0.9999 | 1.0000 | 1.0000 | 0.9998 | 0.9998 |

- **N_f > 64** (none on the scored grid; the frequency pick first reaches 0.99 at 128, measured on the disclosed extension). **N_r = 64** (by seed 64 / 64 / 96 / 64 / 64). Falsifier 1 is RED twice over: N_f > 64, and random reaches 0.99 at 64.
- **Mutant RED** (falsifier 2 holds, round not void): the twin at 64 neurons under the same solve reads 0.0068 (its top-64 by peakiness) and 0.0075-0.0111 (the 5 random 64s); max 0.0111 < 0.5. The trained features, not the solve, carry the accuracy.
- Train accuracy tracks held-out (freq 0.845 / rand 0 1.000 at 64): the frequency cut UNDER-fits, it does not over-fit.

**Verdict: disproved.** The circuit is cuttable to 64 neurons with a closed-form readout and no training (random cuts, 4/5 seeds >= 0.99), but picking by top peakiness, round-robin over the key frequencies, is WORSE than random at every N >= 16, so this pick does not encode the circuit knowledge the claim needed.

## Reading (unmeasured, for the next round)
With 509 of 512 neurons periodic, random picks are already key-frequency neurons, spread over phase and over the (a, b) mixing terms. The top-peakiness neurons of a family are the purest single-frequency responders and are likely near-duplicates (same frequency, similar phase), so N of them span fewer readout directions. A pick that covers phase (e.g. greedy by residual, or by the cos/sin projection angle within each family) is the natural next falsifier. Not measured here.

## Test record (stated per SM's gate, thought-master [fix] 12:41Z)
The tests ran in the private <scratch> venv WITH torch 2.14.0+cpu: cut 7 passed, 0 skipped. The module calls pytest.importorskip("torch"), so WITHOUT torch the whole module SKIPS: a skip is not a pass, and no skipped run is part of this round's record.
