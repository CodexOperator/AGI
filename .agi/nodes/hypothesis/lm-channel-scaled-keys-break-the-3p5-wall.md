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
edited_by: brainstorm
falsifier: If neither per-channel nor bias-subtracted scales gains >=0.10 agreement or >=25 pct KL at 3.5 bits, and the best arm still misses the 0.98/0.02 bars, the 3.5-to-8-bit gap is not primarily a key-scale granularity artifact; stop finer allocation and accept the measured (8,12] wall.
scaffold_hash: cc927f067bf81d91
season: 2
testable_claim: On cached Qwen2.5-0.5B-Instruct, one post-RoPE key arm using per-channel scales or bias-subtracted per-token scales beats token-absmax energy allocation at 3.5 average bits by >=0.10 top-1 agreement and >=25 pct lower mean KL on the same 4096-token held-out OSC.04 eval; at least one variant must reach agreement >=0.75.
tests: "ONE pi parent + ONE kid, slot: ARM4C-light, steps (1) run the existing fixture selftests for rotate-half pairing and post-RoPE hook, (2) reuse osc_band_kquant_a00-86466b78.py and OSC.04 build_eval/metrics on cached Qwen2.5-0.5B, (3) run token-absmax, per-channel, bias-subtracted, and uniform controls at 3.5 bits with scale overhead charged identically, (4) persist agreement, KL, bits, and per-arm sha after every probe, rows to bench/<utc>.jsonl, kid line_ceiling 120."
title: Per-channel or bias-subtracted key scales move the 3.5-bit failure before the 8-bit wall
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-channel-scaled-keys-break-the-3p5-wall

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
