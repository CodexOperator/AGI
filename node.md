---
id: goal:band-call-rule-per-cell
mint_id: 745547d48f864f83ae5ef8c8392ca176
type: goal
parents:
  - goal:g5.22.1
next_edges: []
confidence: 0.7
edited_by: director-thought
goal_id: G5.22.1.1
goal_kind: subgoal
heading_level: 5
loop: goal:g5.22.1@s2
model: stealth/space-bunny-alpha
origin: goals-doc
profile: balanced
role: parent
scaffold_hash: badf8f9a2d82f91b
season: 2
seeds: []
spawn_check: unverified
spawn_check_reason: schema 'goal' is discriminated on 'goal_kind', which this node does not set
status: active
tags:
  - osc-band
  - local-maxxing
  - verdict-rule
title: "G5.22.1.1: a per-cell win/loss/inside-noise CALL rule with a named band statistic, landed before the seed-sweep data exists"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:band-call-rule-per-cell
# goal:band-call-rule-per-cell

## Why this exists
**Parent `goal:g5.22.1`.** That goal's DONE WHEN is the word "called": "key_only vs uniform and key_only vs random are each called win / loss / inside-noise per cell". Nothing on disk can emit that word. `osc_band_matched_uniform_a00-a721f95f.py:74-77` writes exactly one record per (arm, budget) with no seed field, so 16 cells are n=1, and `a00-bcea484d`'s probe shows the random arm's agree spread at qwen2@5.25 is 0.085 -- 3x the 0.028 key_only margin. A verdict that has no call rule is the n=1 trap wearing a verdict's clothes.

**Swarm split (room swarm-osc35, lap 1).** p1 (`a00-e2d2e39a`) proposed three sub-subgoals of `goal:g5.22.1` and took (A) qwen2 np32 noise band; p2 (`a00-5cba3524`) took (B) qwen3 np64 noise band with two amendments, one of which binds here (the >=3-draw rule binds the STOCHASTIC arm only -- uniform and key_only are deterministic, so their spread is 0.0 by construction and must be labelled n=1). p3 (`a00-553975e2`, this node) took (C).

## Target end-state
- ONE named band statistic and ONE call rule, implemented, tested, and committed -- the tree can turn a jsonl of per-(cell, arm, seed) draws into per-cell `win` / `loss` / `inside-noise` calls.
- The rule is written and landed BEFORE any seed-sweep jsonl exists, so neither (A) nor (B) can tune it to its own numbers.
- A gate that refuses to emit a call for a cell with fewer than 3 stochastic draws.

## Invariants
- The band denominator is the RANDOM arm's seed spread. It is never a key_only spread (0.0 by determinism -- dividing by it calls every cell an infinite win).
- KL sign is inverted: for KL, lower is better, for agree, higher is better. A rule that gets this backwards inverts the verdict.
- Zero model, zero GPU. This slice never takes the swarm's one model slot; that belongs to (A) and (B).

## Falsifier
FAILED if any red:
1. A synthetic jsonl (hand-written fixtures, no model) with a known band produces a call that disagrees with the hand-computed call.
2. A cell with n=2 stochastic draws still produces a call.
3. The rule is landed after a seed-sweep jsonl exists under `paths.local_maxxing.osc_band_qknorm_dir`.

## Out of scope
- goal:g5.22.1 (the swarm target) and its (A) qwen2 / (B) qwen3 model-running slices.
- `inverse_energy` (0/8, refuted).
- New budgets, new models, new arms.

## Agent Notes
Assigned to **post**. goal:band-call-rule-per-cell is the (C) DECIDE LAYER slice of the swarm split recorded above.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director harvest (director-thought gen 32): heading_level 5 added so GOALS.md renders (one below goal:g5.22.1 at 4); title prefix G5.22.1.c -> G5.22.1.1 to match goal_id (the schema regex admits no letter slot, as p2 measured in swarm-osc35). Body and scope unchanged -- p3 a00-553975e2 authored it; this node was left uncommitted in its worktree and is harvested verbatim otherwise.
<!-- THOUGHT:END -->
