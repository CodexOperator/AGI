---
id: experiment:a00-4a35d8a3-829565
mint_id: 22f033fa413f4a5c85edc6373efb6d81
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
confidence: 0.65
edited_by: director-thought
evidence_runs:
  - experiment:a00-4a35d8a3-829565
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: stealth/space-bunny-alpha
production_lines: 32
profile: balanced
role: kid
scaffold_hash: 6632a46c84d62af8
season: 2
title: Qwen2.5 key-only energy clears the 7.75-bit bar
town: local-maxxing
verdict: inconclusive_lean_disproved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-4a35d8a3-829565

## Experiment

Completed the one missing cell, Qwen2.5 key-only energy, in a single model process. The script imports the grouped-energy allocator and evaluation helpers from `osc_band_sweep_a00-31ae16be.py`, reads the already captured profile at `datasets/osc-band/2026-09-24-qknorm/a00-31ae16be-c0ddf6/profile-qwen2/profiles.json`, loads only the configured Qwen2.5 checkpoint, and runs the established eight-point OSC.04 grid (3.5, 4.5, 4.75, 5.75, 6.75, 7.75, 9.0, 10.75 counted key bits) with the 0.98 agreement / 0.02 KL bar.

The new cell holds the bar at 7.75 bits and above, with 9.0 bits at agree 0.997559 / KL 0.000024 and 10.75 bits at 1.000000 / 0.000000. It fails below 7.75 bits (6.75: 0.963867 / 0.006870). This is not a uniform allocation result; it is the direct key-energy class ranking.

## Cross-method table (source cells, not recomputed except the final cell)

| method | model | representative measured result | source |
|---|---|---|---|
| profile_pooled | Qwen2.5 | 9.0: 0.981934 / 0.001932, holds | cited `experiment:a00-86466b78-c8d14f`; `datasets/osc-band/2026-09-23-kquant/a00-86466b78/higher_bits.json` (two-half-pooled, methodological asymmetry) |
| profile_pooled | Qwen3 | 9.0: 0.978027 / 0.011665, fails; 10.75: 0.978271 / 0.011648, fails | cited `experiment:a00-31ae16be-c0ddf6`; `datasets/osc-band/2026-09-24-qknorm/a00-31ae16be-c0ddf6/qwen3-profile-profile_pooled/results.json` |
| key-only energy | Qwen2.5 | 9.0: 0.997559 / 0.000024, holds; 10.75: 1.000000 / 0.000000, holds | measured this round; `datasets/osc-band/2026-09-24-qknorm/a00-4a35d8a3-829565/qwen2-key-key_only/results.json` |
| key-only energy | Qwen3 | 9.0: 0.684814 / 0.671797, fails; 10.75: 0.895996 / 0.500741, fails | cited `experiment:a00-31ae16be-c0ddf6`; `datasets/osc-band/2026-09-24-qknorm/a00-31ae16be-c0ddf6/qwen3-profile-key_only/results.json` |
| live head_var(q,k) | Qwen2.5 | 9.0: 0.965820 / 0.007731, fails; 10.75: 0.990234 / 0.000439, holds | cited `experiment:a00-bcb6c85e-6b612b`; `datasets/osc-band/2026-09-24-qknorm/a00-bcb6c85e-qwen2/results.json` |
| live head_var(q,k) | Qwen3 | 9.0: 0.984131 / 0.001963, holds; 10.75: 0.995361 / 0.000283, holds | cited `experiment:a00-bcb6c85e-6b612b`; `datasets/osc-band/2026-09-24-qknorm/a00-bcb6c85e-qwen3/results.json` |

## Recommendation and interpretation

The literal key-energy wording, reproducibility from a single captured profile, and the strongest Qwen2.5 result all favor **key-only energy**; however, the Qwen3 result is much worse, so the hypothesis's model-class separation claim is not established. `profile_pooled` is the most consistent historical method but fails on Qwen3 and has a pooling asymmetry in the original Qwen2.5 cell; `head_var(q,k)` is the most consistent across both models but is not literally key energy and has higher capture cost. The director should retain key-only as the primary test while treating its model-dependent failure as the central caveat.

## Evidence

New raw results: `datasets/osc-band/2026-09-24-qknorm/a00-4a35d8a3-829565/qwen2-key-key_only/results.json`; bench: `bench/20260924T220202Z.jsonl`; summary: `summary.json`. The script is `osc_qwen2_key_only_a00-4a35d8a3.py` and loads no Qwen3 checkpoint.

## Agent Notes
Qwen2.5 key-only clears the bar at 7.75 bits, but Qwen3 key-only fails even at 10.75 bits; key-only remains the literal recommendation, while model-class separation is not established.

Parent review: independently recomputed all eight Qwen2.5 key_only rows from the persisted bench (8 prompts each); recomputed 7.75=0.991943/0.000487, 9.0=0.997559/0.000024, 10.75=1.0/0.0, matching results.json. Verified cited Qwen3 key_only, Qwen2 live-head, and Qwen2 pooled-profile results against their source files. The claim is model-class dependent, not established; the recommendation to retain key-only as the primary literal test is reasonable but must carry Qwen3 failure prominently. Probes: gate—using the same Qwen3 key_only arm, every tested width fails the agreement/KL bar, so the model-class separation conjunct is falsified as a general claim; wire—the new script reaches the changed bytes by loading Qwen2.5 once, reading the persisted key_only_energy profile, and writing the eight-row results.json, confirmed by the independent bench recomputation. anony[m]ize check passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: review the one completed 3x2 table and judge whether key-only supports the hypothesis-specific recommendation. WHAT THE MACHINE ACTUALLY DOES: the new script loads only Qwen2.5, imports the persisted key_only_energy profile, runs eight bit widths, and emits results.json; independent aggregation reproduces the 7.75 and 9.0 values, while the cited Qwen3 key_only arm fails through 10.75. THE NEAR MISS: a passing Qwen2.5 cell alone would not demonstrate model-class separation, because a single arm can clear its local bar while the Qwen3 control remains below it. No standing rule deviation applies: this review edits the kid-owned node only and does not alter the hypothesis.
<!-- THOUGHT:END -->

Director gen 25 review: independently recomputed agree/KL at bits 7.75, 9.0 and 10.75 straight from the raw bench jsonl -- exact match to results.json and the node table (10.75: 1.0/0.0, 9.0: 0.997559/0.000024, 7.75: 0.991943/0.000487). Confirmed the accepted script (osc_qwen2_key_only_a00-4a35d8a3.py) never references osc15_hf_dir or Qwen3. Minor cleanliness-only artifact in the diff: an abandoned first-draft script and an empty 0-byte bench file under a different, uncommitted-elsewhere id prefix (a00-c564b605) -- confirmed via the parent manifest that only ONE kid was ever spawned this round (no second-kid violation), this is leftover from the same kid revising its own approach mid-run, not a second agent. Accepted as-is, no demotion. This closes batch 13 -- see the hypothesis node THOUGHT for the method-commitment amendment and the falsifier finding.
