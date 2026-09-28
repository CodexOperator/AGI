---
id: idea:lm-why-l3-precision-allocation-wall-is-8-12-bits
mint_id: 747d2e22f28e4efda47eaba5d24e2613
type: idea
parents:
  - hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
next_edges: []
edited_by: belam
scaffold_hash: d35bdbcf3da2dafc
scale: small
season: 2
title: WHY does L3 energy-guided key-bit allocation need 8-12 bits, not the hoped 3.5, and does the ranking still earn its keep at that real cost?
town: local-maxxing
---
# idea:lm-why-l3-precision-allocation-wall-is-8-12-bits

# idea:lm-why-l3-precision-allocation-wall-is-8-12-bits

## Idea

WHY does L3's energy-guided KEY precision allocation need ~8-12 bits per
element to clear both quality bars, not the hoped 3.5 bits -- and does the
energy ranking still earn its keep once the ladder pays that real cost, or
does uniform allocation become "good enough" there? scale: small (extension
of the existing LAYERING LADDER chain, town:local-maxxing queue [1] L3).

## Agent Notes

WHY LOOP: hangs on hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
(disproved x3: experiment:a00-b59ee70f-6c45e2 died/abandoned corrective
a00-04dc76fc, experiment:a00-86466b78-c8d14f, experiment:a00-ddd4762f-fc38ef,
experiment:a00-527993c5-67867c), itself downstream of experiment:a00-fa4bb880-d965dd
(OSC.04, PROVED the ranking signal).

WHAT THE FAILURE MEASURED (three independent replications, all on
Qwen2.5-0.5B-Instruct CPU, OSC.04's held-out 4096-token eval):
- a00-86466b78-c8d14f: 3.5-bit bar disproved (energy agreement 0.564, bar
  0.98) -- but energy holds BOTH bars at 9.0 bits; uniform needs 10.25;
  random fails even at 9.0. Energy beats uniform by ~1.25 bits at the
  crossing point -- the ranking signal survives, the budget does not.
- a00-ddd4762f-fc38ef: energy beats uniform at every tested budget from 3.0
  to 12.0 bits, and beats random at 3.5 bits (the only budget with random
  arms); only 12.0 bits holds both bars; safe step lies in (8, 12].
- a00-527993c5-67867c (control arm): energy beats random 2.5-4.4x at
  3.0-3.5 bits, but no budget <= 5.25 bits holds the 0.98/0.02 bars (best
  0.571/1.245 at the tightest budget tried); 16-bit anchor lossless, real
  wall ~8.5-12 bits; CRITICALLY, energy == uniform (no advantage) at the two
  lowest budgets tested (3.25, 2.25 bits) -- the ranking's edge is not
  free at every point, it shows up mid-range and vanishes at the extremes.
- Upstream, OSC.04 (Q-side masking, not K-side bits) already showed the same
  shape: energy beats random 4.5-6x, but zeroing even 3.125 pct of q pairs
  (the gentlest cut) already costs agreement 0.9792 -- 0.08 pt under the 0.98
  bar. Same qualitative result via a different mechanism (drop vs
  requantize): the ranking is real, the cheap end of the budget is not safe.

CANDIDATE CAUSES (from the hypothesis node's own push_further, un-tested):
1. Wrong granularity: per-token absmax on Qwen2.5-0.5B keys is fighting
   outlier channels from k_proj's bias term (this model has no QK-norm).
   Per-channel or bias-subtracted key scales, at the SAME bit budget, may
   close much of the 3.5-to-9 bit gap without spending more bits.
2. Wrong model class: the served Qwen3.5 carries attn_k_norm; a QK-norm
   model may not produce the outlier channels absmax is struggling with, so
   the 3.5-bit wall may be a Qwen2.5-0.5B artifact, not a general one.
3. Baseline miscalibration: round A's "bw4" comparison arm was ternary, not
   a true q4_0-analog blockwise 4-bit baseline -- the uniform comparison
   itself may be understated, which would also understate energy's margin
   over it. Needs re-measurement before any of the above is trusted.

NEXT HYPOTHESIS SHAPE (cheap, CPU/API, reuses OSC.03's energy profiles and
OSC.04's eval/metrics harness already committed to this town):
one arm re-runs the SAME 3.5-bit budget with per-channel or bias-subtracted
key scales (cause 1) against the SAME uniform/random controls, held on
Qwen2.5-0.5B for direct comparability; a second, independent arm repeats the
minimal probe on a QK-norm model (cause 2) at the same budget; a third,
cheapest arm just re-measures the q4_0-analog uniform baseline correctly
(cause 3) since it gates whether the other two arms' margins mean anything.
None of the three needs the GPU rig or a paid model. Falsifier for the
chain: if per-channel/bias-subtracted scales on Qwen2.5-0.5B still can't
clear both bars below ~8 bits, the wall is architectural (RoPE-band energy
ranking a KV cache) rather than a granularity artifact, and L3 should stop
chasing sub-8-bit precision allocation and either accept the 8-12 bit
operating point as the real L3 result, or fold into L4 GEOMETRY (streaming
vs retrieval heads) instead of pursuing finer bit allocation.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Sharpened question: the 3.5-bit claim is dead, but the next decision is whether the measured (8,12]-bit key wall is a Qwen2.5 outlier/granularity artifact or an architectural consequence of post-RoPE attention sensitivity. OSC.10 (experiments a00-86466b78-c8d14f, a00-ddd4762f-fc38ef, a00-527993c5-67867c) measured the why directly: energy beats uniform and same-size random allocations, yet only energy at 9.0 bits holds the 0.98/0.02 bars; a true q4_0-analog baseline was not measured. The open mechanisms are per-channel or bias-subtracted scales, a QK-norm model with attn_k_norm, and correct uniform calibration. Ideas lm-kv-bytes-ledger-q4-cache and lm-kda-constant-state-kv-bytes make the bytes-ledger comparison concrete; hypothesis lm-q4-kv-cache-tg-at-4k supplies a flag-based q4 protocol, and experiments a00-297e744f-32087d / a00-fa4bb880-d965dd show the trade is format/model-specific, not a license for pruning. Inspiration: OSC.04 and OSC.05 establish that zeroing one RoPE pair is already too destructive, while q4 K/V on the served 9B costs only +0.074 pct NLL but has a 35 pct decode penalty; neither settles this 0.5B key allocator. No node should infer an architectural wall until granularity, model class, and baseline calibration are separated.
<!-- THOUGHT:END -->

ADVERSARIAL REVIEW changed all three children, none dropped: (1) true-q4 now supersedes only the proven-ternary bw4 row and does not retroactively erase independent uniform-wall evidence; (2) channel scaling now has the exact logical falsifier and records the partial 4-bit per-channel answer already in experiment:a00-ddd4762f-fc38ef; (3) QK-norm is narrowed to a non-causal model-class probe and remains correctly off-box. The two cached-CPU arms fit <=1 USD with no paid compute; the off-box arm exposes no location or hardware model.
