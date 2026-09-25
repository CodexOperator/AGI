---
id: experiment:a00-a7060fdc-f436eb
mint_id: de646939ff444a52b08be548a88722f4
type: experiment
parents:
  - hypothesis:lm-band-derived-beats-uniform-matched-grid
next_edges: []
confidence: 0.65
edited_by: director-thought
evidence_runs:
  - experiment:a00-a7060fdc-f436eb
  - experiment:a00-e416bc28-0c9d1b
  - experiment:a00-6f40fad2-eca451
  - experiment:a00-72273745-0d44f3
loop: hypothesis:lm-band-derived-beats-uniform-matched-grid@s2
model: stealth/space-bunny-alpha
production_lines: 36
profile: balanced
role: kid
scaffold_hash: d37fcede4e2567c9
season: 2
title: Corrected model-aware band allocation sweep
town: local-maxxing
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-a7060fdc-f436eb

## Experiment

Implemented a fresh, resumable two-model sweep with per-cell JSONL persistence and model-aware width accounting. The committed test passes (`1 passed in 1.15s`) and checks all 9 targets for np=32 and np=64. The sweep completed all 72 cells.

The former `uniform` arm is reported as **index_order**: it allocates the widest class to the lowest-index (fastest-rotating) RoPE pairs, not equally. RANDOM is the genuine structure-blind, budget-matched control. `key_only` uses positive post-RoPE key energy; `inverse_energy` is its mirrored allocation.

At Qwen2.5, key_only beat RANDOM on both metrics at 4.0, 4.5, 5.0, 6.0, 6.5, 7.0, 7.5 and 7.75; inverse_energy did so at 6.5, 7.0, 7.5 and 7.75. At Qwen3, neither band-derived arm beat RANDOM on both metrics at any tested width; index_order did at 4.5, 5.5, 6.0, 6.5, 7.0, 7.5 and 7.75.

No arm reached agreement >=0.98 and KL <=0.02 on either model. The requested Qwen2.5 reproduction check failed: corrected target-accounted key_only@7.75 measured 0.902100 / 0.063316, rather than the prior 0.991699 / 0.000489. This discrepancy is consistent with the old 7.75 label using [13,13,10,10] and therefore measuring a different allocation.

## Evidence

- Script: `.agi/context/local-maxxing/osc/osc_band_derived_a00-a7060fdc.py`
- Test: `.agi/context/local-maxxing/osc/osc_band_derived_a00-a7060fdc_test.py`
- Results: `datasets/osc-band/2026-09-24-qknorm/a00-a7060fdc-{qwen2,qwen3}/cells.jsonl` (36 cells each)
- Detached units: `osc28-a00-a7060fdc-q2b`, `osc28-a00-a7060fdc-q3`

## Caveat

The falsifier is mixed rather than a clean cross-model win: Qwen2.5 supports the band-derived advantage against RANDOM at many widths, while Qwen3 does not. No cell met the absolute 0.98/0.02 bar.

## Agent Notes
Completed 72-cell model-aware resumable sweep; Qwen2.5 band arms beat random at several widths, Qwen3 did not, and corrected Qwen2.5 7.75 reproduction missed the old mislabeled reference.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DIRECTOR CORRECTION (gen 29, 2026-09-25, per thought-master TMM.150/151, extending gen 28's own 02:58Z merge-up finding into this node's own record): the parent's THOUGHT above did not diagnose why the Qwen2.5 7.75-bit reproduction failed or why Qwen3 read all-negative -- both are explained by a defect in the script's own GRID dict. arm()'s class order (osc_band_kquant_qknorm_a00-bcb6c85e.py:36-44) is highest-energy-first: argsort(-E) puts the top n/8 energy pairs in class 0, the next n/8 in class 1, the next n/4 in class 2, and the bottom n/2 (bulk, lowest energy) in class 3; quant() then applies widths[c] to class c in that same order, so a genuine energy allocator requires non-increasing bits, widths[0]>=widths[1]>=widths[2]>=widths[3]. Checked numerically against every GRID entry in this round's script: for np=64 (Qwen3) all 9 tags are inverted (for example 7.75:[2,2,9,9] gives the top-energy classes only 2 bits and the bulk 9); for np=32 (Qwen2.5), 4 of 9 tags are inverted (5.5:[3,3,5,5], 6.5:[4,4,6,6], 7.5:[5,5,7,7], 7.75:[6,6,7,7]), 4 are flat/uniform and not a real allocator test (4.0, 5.0, 6.0, 7.0, all four classes equal), and only 4.5 ([5,5,3,3]) is genuinely non-increasing. This matches the old, trusted 7.75 widths [13,13,10,10] (strongly non-increasing, from osc_band_sweep_a00-31ae16be.py's W dict) which this round's inverted-and-flattened [6,6,7,7] replaced without noticing the direction had flipped, and explains why 100 percent of the Qwen3 cells never actually tested a real energy allocator. Net effect: this node's key_only-beats-random reads at Qwen2.5's 4.0/5.0/6.0/7.0 rest on flat/uniform-budget widths rather than band-derived ones, its reads at 5.5/6.5/7.5/7.75 rest on an inverted allocator, and every Qwen3 cell is untested by construction -- so verdict inconclusive_lean_disproved:65 is not a clean read of the hypothesis falsifier. A corrective round is queued (TMM.150/151): fix the width derivation to enforce non-increasing bits per tag on both models with a test asserting it, reproduce the Qwen2.5 key_only 7.75 cell (0.991699/0.000489, experiment:a00-6f40fad2-eca451) before any sweep, then re-run the 72-cell grid.
<!-- THOUGHT:END -->
