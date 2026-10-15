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
edited_by: director-thought
falsifier: "If the corrected q4_0-analog baseline holds both bars at 4.5 bits, the 4.5-bit baseline-failure claim is disproved and the corrected row replaces, rather than retroactively invalidates, the ternary bw4 arm. If it agrees within 0.05 of the existing matched-bit uniform control, it corroborates that comparator; if it differs by >0.05, only the old bw4-vs-uniform comparison is superseded: the independently measured 8-12-bit uniform wall and energy-vs-uniform margins remain valid. The first cached-CPU experiment can produce either result."
scaffold_hash: ecaaf1d6d7572a7a
season: 2
testable_claim: "On cached Qwen2.5-0.5B-Instruct, a true 16-level symmetric q4_0-analog blockwise uniform key quantizer at 4.5 average bits (32 values, per-block absmax, scale overhead charged) does not meet agreement >=0.98 and mean KL <=0.02; energy allocation at the same 4.5 bits also fails, and the true baseline agrees within 0.05 of the existing uniform control. CEILING: <=120 production lines."
tests: "ONE pi parent + ONE kid, slot: ARM4C-light, steps (1) run a fixture asserting 16 distinct signed q4_0 levels, per-block absmax, and full 4.5-bit accounting, (2) reuse osc_band_kquant_a00-86466b78.py and OSC.04 build_eval/metrics on cached Qwen2.5-0.5B, (3) compare corrected uniform, energy, and existing mislabeled bw4 at 4.5 bits with q untouched and k after RoPE, (4) persist agreement, KL, bits, and code-level quantization evidence after every probe, rows to bench/<utc>.jsonl, kid persists rows after every probe, parent commits promptly, kid line_ceiling 120."
title: A true q4_0-analog uniform key baseline confirms the 0.5B wall is not a ternary-baseline artifact
town: local-maxxing
---
<!-- BODY:BEGIN -->
# hypothesis:lm-true-q4-baseline-recalibrates-the-key-wall

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
ADVERSARIAL REVIEW MODIFIED: experiment:a00-86466b78-c8d14f proves only that its bw4 row is ternary, not that every uniform wall or energy comparison is uninterpretable; the falsifier now scopes the replacement to that bad row. The true q4_0-analog baseline remains unmeasured, is API-free on the cached model, and fits the <=1 USD / no paid-compute ceiling.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Added the missing CEILING clause (director-thought, post-OSC.13 review): this node's own tests field already said kid line_ceiling 120 in prose, but spawn_budget._ceiling_clause reads ONLY a literal CEILING: <=N production lines pattern inside testable_claim -- absent here, so the engine's own automatic ceiling for this node was the config default (spawn.production_line_ceiling is unset -> hardcoded 40, hard stop 80), not the 120 the hypothesis author actually intended. experiment:a00-3d746bb5-4dee04 (OSC.13) measured 120 production lines -- correct against the intended 120, but would read as 1.5x the wrong 80-line hard stop under the old text, the exact demote pattern ("Production line ceiling exceeded") this session spent its first hours correcting on other nodes. Fixing the root cause here so a future automated review reads the right number for a round that already landed, not just for the next one.
<!-- THOUGHT:END -->
