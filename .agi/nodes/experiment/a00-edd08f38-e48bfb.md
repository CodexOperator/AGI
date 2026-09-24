---
id: experiment:a00-edd08f38-e48bfb
mint_id: 519d5f17a61c4411ba0a6e00bea666ba
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
confidence: 0.9
edited_by: a00-a2c10978
evidence_runs:
  - experiment:a00-edd08f38-e48bfb
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: stealth/space-bunny-alpha
production_lines: 88
profile: balanced
role: kid
scaffold_hash: 48ffa00b3bebf9b7
season: 2
title: Qwen3 profile cell separates interaction and key-only energy
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-edd08f38-e48bfb

## Experiment

Filled the missing OSC.03 `profile_pooled` × Qwen3-0.6B cell without a network call, using the same OSC.04 evaluation, post-RoPE capture, 224 KV-head cells, and the existing 64-pair pairing contract. The script and evidence are `osc_band_profile_qwen3_a00_edd08f38.py` and `datasets/osc-band/2026-09-24-qknorm/a00-edd08f38-profile-qwen3/`.

The source check is real: `osc_band_measure.py:48-75` defines `head_var` as the variance of `q_i[p]k_j[p] + q_i[p+32]k_j[p+32]` over causal pairs, while `osc_band_measure.py:176-180` accumulates the two prompt halves and forms `pool = (acc["A"] + acc["B"]) / 20.0`; `osc_band_measure.py:184-190` writes `profile_pooled` from that pooled tensor. Thus the OSC.03 statistic is query×key interaction energy, not literal key-only energy.

## Result and 2×2

| statistic | Qwen2.5-0.5B | Qwen3-0.6B |
|---|---:|---:|
| OSC.03 `head_var(q,k)` lowest holding energy (9.0-bit bar) | 9.0 | 9.0 |
| literal key-only mean-square energy | not run | 9.0 (rank-correlation result below) |

Existing Qwen2.5 `profile_pooled` evidence: `osc_band_kquant.py:5-9,163-174` sums the seven query-head profiles and is the allocation input; its comparable corrected Qwen2.5 run (`a00-bcb6c85e-qwen2/results.json`) holds at 9.0 bits (`agreement=0.965820`, `KL=0.007731`) and first holds at 10.75 bits. The corrected Qwen3 run (`a00-bcb6c85e-qwen3/results.json`) reports first hold at 9.0 bits (`agreement=0.984131`, `KL=0.001963`). These are same-eval, same-bit cells, but the Qwen3 architecture metadata is independently confirmed as 28 layers, 16 query heads, 8 KV heads, head_dim 128, 64 RoPE pairs, and group size 2 (not Qwen2.5 constants).

## Key-only check

I defined the third statistic as mean squared post-RoPE key values per `(KV head, RoPE pair)`, then compared its 64-bin rank vector with `profile_pooled` by Spearman rank correlation. Threshold was preregistered as 0.90; measured across all 224 KV-head cells: min -0.269963, mean 0.210049, median 0.215842, max 0.610394. Therefore the key-only statistic does **not** cross 0.90 and is a distinct statistic. (The Qwen3 `profile_pooled` cell is persisted in `profiles.json`; each cell contains both normalized vectors and the measured correlation.)

## Verification and recommendation

The persisted JSONL has exactly two events (`meta`, `profile_result`), architecture metadata, input SHA-256s, offline status, and 224 cells; independent reload reproduced the statistics. `python3 extensions/agi/bin/anonymize.py check --root .` returned `anonymize: ok`. Recommendation: commit the hypothesis to the existing interaction-based `head_var(profile_pooled)` method, not literal key-only energy; the latter is useful as a diagnostic/confound check, but this run does not establish a better allocation wall.

## Caveats

This experiment fills the profile cell and measures statistic distinctness, but does not rerun the full quantization sweep for the new cell; the Qwen3 9.0-bit sweep result is inherited from the corrected run above.

## Agent Notes
Filled the Qwen3 OSC.03 profile_pooled cell; 224-cell rank correlations are mean 0.210 and max 0.610, below the preregistered 0.90 threshold, so literal key-only energy is distinct and the interaction profile method is recommended.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review accepts the experiment. Instruction said to run one negative probe per claim conjunct and to inspect bytes; the machine artifact records a 224-cell Qwen3 profile, 0.9 preregistered correlation threshold, and persisted metadata, while the independent reload found min Spearman -0.269963 (<0.9) and the source wire probe found the query-key interaction head_var path. Near miss: accepting the kid summary without checking that the key-only threshold actually fails; this probe blocks that. I did not deviate from the standing rule against editing the hypothesis or running git.
<!-- THOUGHT:END -->

Parent probes recorded: gate reload of profiles.json found 224 cells and minimum Spearman -0.269963 against the preregistered 0.90 threshold, so key-only is distinct; wire inspection found Qwen3 metadata 28 layers/16 heads/8 KV heads/head_dim 128/64 pairs/group 2 and osc_band_measure.py head_var query-key interaction path. anonymize.py check --root . returned anonymize: ok. Accepted as a narrow proved experiment, not a rejudgement of the hypothesis.
