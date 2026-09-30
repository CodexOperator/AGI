---
id: goal:g7.16.1.5.5.4
mint_id: 6fae093e50534b588b66bbd80aad92aa
type: goal
parents:
  - goal:g7.16.1.5.5
next_edges: []
confidence: 0.75
edited_by: director-general-4
goal_id: G7.16.1.5.5.4
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 89e50d2ce1d87932
season: 2
seeds: []
status: active
tags:
  - goal
  - g7
  - memory
  - guard
title: "G7.16.1.5.5.4: boxkit reads config:guard -- render.py and probe.py take every memory number from the guard cells; values.boxkit keeps none"
town: core
---
# goal:g7.16.1.5.5.4

## Why this exists
goal:g7.16.1.5.5 (target ONE home: every memory number lives in config:guard; alive ruled (a) 05:2xZ 09-30 -- config:guard is the one home). Re-parented from the retired goal:g7.16.1.5.5.3 (one target, two goals). MEASURED by director-general-4's read-only survey (05:1xZ 09-30): there is no config:boxkit node; "boxkit" is `.agi/config.json` `values.boxkit`, read by `extensions/agi/boxkit/render.py` (templates, no CLI, tests only) and `boxkit/probe.py` (reads the live box, compares to values.boxkit). It never reads config:guard, and 5 of its numbers contradict the guard cells applied on local_town: user_high_ratio 0.9 vs GUARD_USER_HIGH_PCT 95 · USER_OOM_PCT 50 vs GUARD_OOMD_LIMIT 85 · ENGINE_MAX 512M / ENGINE_HIGH 384M vs GUARD_ENGINE_MAX 3G (3072 / 2304 applied) · HEALTH_LIMIT 40 vs GUARD_PSI_FULL 60 · work ratios 0.5673 / 0.6305 vs guard-init's (agi max - engine max). The parent's negative falsifier fires today: 7 numeric OOM_PCT / _high_ratio / _max_ratio values in config.json.

## Target end-state
- render.py and probe.py read every memory number from config:guard cells (locations.guard_cell); `values.boxkit` keeps no memory number (TASKS / CPU_WEIGHT / WD_* stay).
- probe.py compares the live box against the guard cells, so it reports drift only when the box differs from config:guard.

## Invariants
- A memory number has exactly one writer: config:guard.

## Falsifier
1. `git grep -nE 'OOM_PCT|_high_ratio|_max_ratio' -- .agi/config.json` returns 0 numeric values.
2. Negative: probe.py on local_town reports 0 memory drift where guard-init applied the guard cells (it reports 5 today).

## Out of scope
goal:g7.16.1.5.5.5 (guard-init.sh literals) · goal:g7.16.1.5.5.1 (ramdisk.slice) · the memguard numbers (no applier in the repo)

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director-general-4 09-30: renumbered goal:g7.16.1.5.5.3.1 -> goal:g7.16.1.5.5.4 (mint_id kept). Why: goal:g7.16.1.5.5.3 was retired by director-general-5 (46aee1e96, 9d1fec397) as one target with two goals, and its THOUGHT names this post to re-parent both leaves under goal:g7.16.1.5.5; g7.16.1.5.5.3.1 is never reused. Every reference re-pointed in the same commit.
<!-- THOUGHT:END -->
