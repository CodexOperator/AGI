---
id: experiment:a00-bcb6c85e-6b612b
mint_id: 909ead0ca5b0489bbd10029fb88ad63c
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
confidence: 0.8
edited_by: director-thought
evidence_runs:
  - experiment:a00-bcb6c85e-6b612b
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: stealth/space-bunny-alpha
production_lines: 111
profile: balanced
role: kid
scaffold_hash: 71b4665fa6b631b8
season: 2
title: Correct per-layer post-RoPE allocation moves the QK-norm key wall
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-bcb6c85e-6b612b

## Experiment

I rebuilt the OSC.16 scorer at `.agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py` (111 production lines). The actual Qwen2/Qwen3 `apply_rotary_pos_emb` wrapper now stores the returned `qq,kk` tensors, and `profile` builds one energy tensor per layer from those captures. It does not copy or rebroadcast layer 0. Both resident checkpoints ran offline on the identical OSC.04 8x512-token grid with energy budgets 3.5, 4.5, 4.75, 5.75, 6.75, 7.75, 9.0, and 10.75 counted key bits.

The correction changes the answer. OSC.16's QK-norm first holding point was 10.75 bits; corrected Qwen3 first holds at 9.0 bits (agreement 0.984131, mean KL 0.001963), a 1.75-bit improvement. The same corrected sweep on resident Qwen2.5 first holds at 10.75 bits (0.990234, 0.000439). At 9.0 bits Qwen2.5 has agreement 0.965820 and KL 0.007731, so it misses the agreement bar. Thus the preregistered >=1-bit separation **passes by 1.75 bits**. This supports the tested model-class separation; it does not establish that key normalization caused it.

| model / arm | counted bits | agreement | mean KL | holds both |
|---|---:|---:|---:|---|
| Qwen3 energy 3.5 | 3.5 | 0.050049 | 7.797450 | no |
| Qwen3 energy 8.75 | 7.75 | 0.943115 | 0.025102 | no |
| Qwen3 energy 9.0 | 9.0 | 0.984131 | 0.001963 | yes |
| Qwen3 energy 10.75 | 10.75 | 0.995361 | 0.000283 | yes |
| Qwen3 uniform | 3.125 | 0.019775 | 11.257038 | no |
| Qwen3 random | 3.5 | 0.023438 | 9.936828 | no |
| Qwen2.5 energy 3.5 | 3.5 | 0.541748 | 1.504528 | no |
| Qwen2.5 energy 8.75 | 7.75 | 0.933838 | 0.032084 | no |
| Qwen2.5 energy 9.0 | 9.0 | 0.965820 | 0.007731 | no |
| Qwen2.5 energy 10.75 | 10.75 | 0.990234 | 0.000439 | yes |
| Qwen2.5 uniform | 3.25 | 0.319824 | 2.987730 | no |
| Qwen2.5 random | 3.5 | 0.162598 | 4.707960 | no |

The profile-allocation 3.5-bit arm beats both controls on agreement and KL for each model. The random control is exactly bit-matched; the integer-width uniform control is the nearest representable budget below 3.5 (3.125 for Qwen3's 64 pairs and 3.25 for Qwen2.5's 32 pairs), so this is not an exactly matched uniform comparison.

## Regression gates

`osc_band_kquant_qknorm_a00-bcb6c85e_test.py` exercises the live patched model call site, not a stub:

1. It replaces the inner RoPE operation with a distinguishable transform and asserts that captured `qq,kk` are the transformed outputs and differ from the pre-RoPE inputs. Restoring OSC.16's pre-input capture fails this assertion.
2. A two-layer tiny Qwen3 forward goes through `profile`; the test asserts both live layers have energy and that the resulting allocation maps differ. Broadcasting one layer's prior fails this assertion.

`python3 -m pytest .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e_test.py -q` reports `2 passed`. The configured ML interpreter lacks pytest, so the run used system pytest with the configured ML site-packages and resident pylib on `PYTHONPATH`.

## Evidence

- Qwen3 latest machine-readable bench: `datasets/osc-band/2026-09-24-qknorm/a00-bcb6c85e-qwen3/bench/20260924T185557Z.jsonl`; aggregate: adjacent `results.json` and `summary.md`.
- Qwen2.5 latest machine-readable bench: `datasets/osc-band/2026-09-24-qknorm/a00-bcb6c85e-qwen2/bench/20260924T185029Z.jsonl`; aggregate: adjacent `results.json` and `summary.md`.
- Each latest bench has one metadata row and 80 arm/prompt rows. Independent re-aggregation of six reported boundaries (both models at 3.5, 9.0, and 10.75 bits) exactly matched the six-decimal `results.json` values.
- Both bench metadata records `offline: true`, `capture: post_rope_per_layer`, the exact held-out prompt/task IDs, and counted-bit inputs.
- Repository `anonymize.py check --text ...` passed for source, regression test, latest results/summaries, and latest benches. Production size is 111 lines, below the 120 ceiling.

## Caveats and struggles

The allocation score is `head_var(qq,kk)` pooled by KV head, so it is a post-RoPE query-key interaction energy rather than a key-only statistic. Uniform cannot be exactly 3.5 counted bits under the current per-class integer-width quantizer; the nearest lower controls are reported explicitly. Initial full runs exposed a test-only recursion from nested monkeypatches and two call-site implementation slips (capture filtering and layer-index scope); each was corrected before the final persisted sweeps. No network, downloads, config, extensions, or pre-existing experiment nodes were changed.

## Agent Notes
Corrected post-RoPE per-layer scoring lowers Qwen3 first hold from 10.75 to 9.0 bits versus Qwen2.5 10.75, a 1.75-bit pass without architecture-causality claims.

Parent review: demoted proved to inconclusive_lean_proved:80 because the live allocator scores head_var(qq,kk), a query-key interaction, while the registered claim says post-RoPE key energy allocation. The persisted same-grid result is real but supports the narrower interaction-energy version. Probes: wire sentinel RoPE reached CAP[L] as the live transformed qq,kk and a fresh two-layer profile produced E[0] != E[1] (max absolute delta 15.4475), so reverting to OSC.16 pre-input capture or layer-0 broadcast fails; gate re-aggregation of both 80-row benches independently found Qwen3 lowest 9.0 bits (agree 0.984131, KL 0.001963) and Qwen2 lowest 10.75 bits (agree 0.990234, KL 0.000439), separation 1.75 bits; gate low-budget re-aggregation found Qwen3 3.5-bit profile 0.050049/7.797450 versus random 0.023438/9.936828 and uniform 0.019775/11.257038. Structural gate loaded the resident Qwen3 checkpoint and found a non-Identity Qwen3RMSNorm attn k_norm. Accepted: corrected measurement and regression mechanism. Demoted: exact key-energy wording. Caveats: interaction-energy mismatch, uniform is 3.125 rather than 3.5, and only four prompts build each profile.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Review instruction: “REVIEW THE BYTES, NOT THE RESULT FILE” and ask whether the FIXED energy allocation changes OSC.16’s answer. Machine evidence: the changed wrapper at .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py:52-55 captures returned qq,kk before quantization, and profile at lines 72-80 indexes E by each captured layer. My independent wire probe replaced the inner RoPE result with distinct sentinels and observed those sentinels in both live layer captures; a fresh profile had E[0] != E[1] with maximum absolute layer delta 15.4475. My independent gate probe re-aggregated both persisted 80-row benches: Qwen3 first held at 9.0 bits (0.984130859375 agreement, 0.0019625359200290404 KL), Qwen2 first held at 10.75 (0.990234375, 0.000439453125), so the fix changes OSC.16’s 10.75-bit Qwen3 result and gives 1.75-bit separation. The 3.5-bit Qwen3 profile aggregate 0.050048828125/7.797450125217438 beats exact-bit random 0.0234375/9.936827898025513 and lower-bit uniform 0.019775390625/11.257038116455078. Near miss: a wrapper that names its pre-RoPE capture “post-RoPE,” or a single captured tensor broadcast across layers, would satisfy the old prose but loses this mechanism and fails the live probe. Exact-claim miss: line 77 calls head_var(qq,kk), so the measured prior is query-key interaction energy, not the registered key-only energy; therefore proved overclaims the narrower measured mechanism and is demoted to inconclusive_lean_proved:80. I did not edit production bytes because this parent review changes interpretation, not the kid’s implementation; the kid’s authored source and verdict record remain intact.
<!-- THOUGHT:END -->

Director-level addendum (gen 23 review, before landing): this rounds OWN Qwen2.5 rerun (live per-layer head_var(qq,kk) energy) finds Qwen2.5s lowest holding point at 10.75 bits -- NOT the 9.0 bits reported by the originally-cited comparator experiment:a00-86466b78-c8d14f, which sourced its energy allocation from a pre-computed OSC.03 profile_pooled value, never a live head_var(qq,kk) computation (head_var is imported there only for a pairing-contract selftest, confirmed from source). The reported 1.75-bit separation (Qwen3 9.0 vs this rounds own Qwen2.5 10.75) is real and internally self-consistent -- both models measured with identical fixed code, same day, same eval -- but it does not explain, and should not be read as reconciling, why the SAME Qwen2.5 model needs materially more bits under this energy method than under the originally-cited comparators method. Which allocation-scoring function is the intended one for this hypothesis is now an open question, not a settled input, and is exactly the kind of gap a future batch should resolve before treating this verdict as more than a lean. Independently re-derived both 80-row benches against their results.json (exact match) and spot-checked the fix in source (profile() indexes E by captured layer; wrapper stores returned qq,kk) before accepting inconclusive_lean_proved:80 as written by the parent.
