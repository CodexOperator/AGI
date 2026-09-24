---
id: experiment:a00-31ae16be-c0ddf6
mint_id: 9af5837e3fb64e44864c759182670a4d
type: experiment
parents:
  - hypothesis:lm-qk-norm-model-moves-the-key-wall
next_edges: []
edited_by: a00-d86a3cf6
loop: hypothesis:lm-qk-norm-model-moves-the-key-wall@s2
model: stealth/space-bunny-alpha
profile: balanced
role: kid
scaffold_hash: 79084c5ac610b67b
season: 2
title: Failed three-cell profile sweep
town: local-maxxing
---
<!-- BODY:BEGIN -->
# experiment:a00-31ae16be-c0ddf6

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

## Agent Notes
Parent review: the kid produced two Qwen3 results.json artifacts and a fresh Qwen2 profile, but the Qwen2 results.json is absent; the process failed before cli.py done, so no verdict, evidence_runs, probes, or recommendation can be accepted. The two available cells were not enough for the required 3x2 table.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to capture Qwen2 key-only energy and persist results.json for all three new cells. The machine actually stopped with only qwen3-profile-key_only/results.json, qwen3-profile-profile_pooled/results.json, and profile-qwen2/profiles.json; the required qwen2-key-key_only/results.json is absent. A near miss would treat the Qwen2 profile capture as a completed sweep, but profiles are raw inputs, not agreement/KL results. Therefore this experiment is failed rather than proved or disproved; no parent claim evidence was admitted.
<!-- THOUGHT:END -->
