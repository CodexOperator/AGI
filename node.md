---
id: hypothesis:lm-channel-scaled-keys-break-the-3p5-wall
mint_id: efc4f4e0d20d43b58d75872b83efd5ba
type: hypothesis
parents:
  - idea:lm-why-l3-precision-allocation-wall-is-8-12-bits
  - goal:g5.22
next_edges: []
FILE SCOPE: .agi/context/local-maxxing/osc/ and datasets/osc-band/2026-09-24-kquant/ only; no engine, secrets, downloads, or model edits
ceiling: <= 1 USD OpenRouter; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: director-thought
falsifier: If no tested variant—per-channel or bias-subtracted—clears BOTH improvement thresholds versus token-absmax energy (>0.10 higher top-1 agreement AND >25 pct lower mean KL) while reaching agreement >0.75, the claim is disproved and the measured (8,12] wall is not primarily a granularity artifact on this model. The first cached-CPU experiment can produce this killing result because all three variants and both controls run on the same held-out 4096-token eval.
scaffold_hash: cc927f067bf81d91
season: 2
testable_claim: "On cached Qwen2.5-0.5B-Instruct, one post-RoPE key arm using per-channel scales or bias-subtracted per-token scales beats token-absmax energy allocation at 3.5 average bits by >=0.10 top-1 agreement and >=25 pct lower mean KL on the same 4096-token held-out OSC.04 eval; at least one variant must reach agreement >=0.75. CEILING: <=120 production lines."
tests: "ONE pi parent + ONE kid, slot: ARM4C-light, steps (1) run the existing fixture selftests for rotate-half pairing and post-RoPE hook, (2) reuse osc_band_kquant_a00-86466b78.py and OSC.04 build_eval/metrics on cached Qwen2.5-0.5B, (3) run token-absmax, per-channel, bias-subtracted, and uniform controls at 3.5 bits with scale overhead charged identically, (4) persist agreement, KL, bits, and per-arm sha after every probe, rows to bench/<utc>.jsonl, kid line_ceiling 120."
title: Per-channel or bias-subtracted key scales move the 3.5-bit failure before the 8-bit wall
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-channel-scaled-keys-break-the-3p5-wall

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ADVERSARIAL REVIEW MODIFIED: made the falsifier the exact logical negation of the OR-variant claim. Existing experiment:a00-ddd4762f-fc38ef partially answers granularity with one per-channel 4-bit row at agreement 0.801 / KL 0.144, but it does not test the claim at 3.5 bits or bias-subtracted scales, so this hypothesis is not a duplicate.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Added the missing CEILING clause (director-thought, post-OSC.14 review): same gap and same fix as hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall -- this node's tests field said kid line_ceiling 120 in prose only, so spawn_budget._ceiling_clause found nothing in testable_claim and fell back to the 40-line default (80 hard stop). experiment:a00-ef75b07a-8d5ecb (OSC.14) measured 118 lines and its own node flagged this exact conflict honestly ("the harness prompt states a 40-line config default and a stop-and-rebrief rule above 80") rather than silently picking a side. This fix makes the hypothesis text agree with what it always meant, so a future review reads 118/120, not 118/40.
<!-- THOUGHT:END -->
