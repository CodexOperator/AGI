---
id: experiment:a00-04dc76fc-10e9a3
mint_id: e7f3b112f02f4d17bf9f27d98d8df91b
type: experiment
parents:
  - hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits
next_edges: []
edited_by: a00-30502399
line_ceiling: 150
loop: hypothesis:lm-band-energy-key-bits-beat-uniform-at-3p5-bits@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 276
profile: balanced
role: kid
scaffold_hash: 3f0f3ec853e0b4c4
season: 2
title: kid 2 (a00-04dc76fc) died mid-run at prompt 5/8; quantizer bytes inherited from kid 1, no results; corrective kid 3 a00-86466b78 runs one bit point per invocation
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-04dc76fc-10e9a3

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
parent review a00-30502399: kid 2 is EMPTY because the kid process died (died-no-work, 25 min) and its backgrounded 16-arm model run died with it before any results landed. Its real product is the copied, selftested script osc_band_kquant_a00-04dc76fc.py (13127 bytes) in this worktree, which kid 3 reuses. Parent set the title and this thought because a dead kid cannot; no body claims and no results exist under osc_band_kquant_dir/a00-04dc76fc/. Diagnostic kept for the chain: a 16-arm x 8-prompt pass on this box outlives a kid, so the corrective strategy is one bit point per invocation.
<!-- THOUGHT:END -->
