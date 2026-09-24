---
id: hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall
mint_id: e1458a19dee14fc0ae3ea2546601ddf8
type: hypothesis
parents:
  - idea:lm-why-l3-precision-allocation-wall-is-8-12-bits
  - goal:g5.22
next_edges: []
FILE SCOPE: .agi/context/local-maxxing/osc/ and datasets/osc-band/2026-09-24-q4/ only; no engine, secrets, downloads, or model edits
ceiling: <= 1 USD OpenRouter; 0 compute; no downloads on ARM4C without an owner yes; runs <= 10 min
edited_by: brainstorm
falsifier: If the corrected q4_0-analog baseline holds both bars at 4.5 bits, or differs from the existing uniform control by >0.05 agreement, the prior 8-12 bit wall and energy-vs-uniform margin are uninterpretable; rerun the comparison with the corrected baseline before any allocation claim.
scaffold_hash: ecaaf1d6d7572a7a
season: 2
testable_claim: On cached Qwen2.5-0.5B-Instruct, a true 16-level symmetric q4_0-analog blockwise uniform key quantizer at 4.5 average bits (32 values, per-block absmax, scale overhead charged) does not meet agreement >=0.98 and mean KL <=0.02; energy allocation at the same 4.5 bits also fails, and the true baseline agrees within 0.05 of the existing uniform control.
tests: "ONE pi parent + ONE kid, slot: ARM4C-light, steps (1) run a fixture asserting 16 distinct signed q4_0 levels, per-block absmax, and full 4.5-bit accounting, (2) reuse osc_band_kquant_a00-86466b78.py and OSC.04 build_eval/metrics on cached Qwen2.5-0.5B, (3) compare corrected uniform, energy, and existing mislabeled bw4 at 4.5 bits with q untouched and k after RoPE, (4) persist agreement, KL, bits, and code-level quantization evidence after every probe, rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, kid line_ceiling 120."
title: A true q4_0-analog uniform key baseline confirms the 0.5B wall is not a ternary-baseline artifact
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
