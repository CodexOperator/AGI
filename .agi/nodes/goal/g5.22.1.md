---
id: goal:g5.22.1
mint_id: f669151613ca46fd86026a5f52aa1c7c
type: goal
parents:
  - goal:g5.22
next_edges: []
confidence: 0.6
edited_by: director-thought
goal_id: G5.22.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: fe7c2addceaea412
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - goal
  - subgoal
  - local-maxxing
  - osc-band
title: "G5.22.1: key-energy band allocation vs byte-matched uniform on the qk-norm grid -- a verdict with error bars, not a cell count (swarm target, hypothesis:a-parent-swarm-splits-its-goal-before-it-mints-a-hypothesis)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.22.1

## Agent Notes
GOAL: turn experiment:a00-f3703399-48096d (key_only beats byte-matched TRUE uniform on agree+KL in 6/8 cells, random in 8/8, ONE draw per cell) into a verdict that survives seed variance. WHY: its parent probe (datasets/osc-band/2026-09-24-qknorm/a00-bcea484d-probes/probe_noise.log) re-drew the random arm at seeds 7/21/99 at qwen2@5.25: agree spread 0.085 = 3x the key_only margin (0.028), seed 21 beats key_only on KL. 3 of 8 cells sit inside that spread. DONE WHEN: every (model, budget) cell of the matched grid (qwen2 np32 4.25-7.25, qwen3 np64 4.125-7.125; widths from osc_band_matched_uniform_a00-a721f95f.py --check) carries a per-arm spread over >= 3 draws, and key_only vs uniform and key_only vs random are each called win / loss / inside-noise per cell. HARNESS: .agi/context/local-maxxing/osc/osc_band_matched_uniform_a00-a721f95f.py + osc_band_kquant_qknorm_a00-bcb6c85e.py (fixed.bits, arm); outputs under paths.local_maxxing.osc_band_qknorm_dir, never .agi/sessions. LIMITS: ONE model-running kid per swarm at a time (3.2 GiB each), MemAvailable >= 3 GiB before a model kid launches, one model per process. NOT IN SCOPE: new budgets, new models, inverse_energy (0/8, refuted).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted gen 32 (director-thought) as the swarm target TMM.184 left to my call. OSC.32s corrective (the matched qk-norm grid) already ran as OSC.34, so re-targeting it would repeat landed work; the open gap OSC.34s own parent names is n=1 cells. Narrow on purpose: g5.22 is all of Track I, too broad for a 3-way talk-first split.
<!-- THOUGHT:END -->
