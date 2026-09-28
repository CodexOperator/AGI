---
id: goal:g7.33.9.1
mint_id: 183d7f2752594849b14d6cf11191109a
type: goal
parents:
  - goal:g7.33.9
next_edges: []
confidence: 0.9
edited_by: belam
goal_id: G7.33.9.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
role: prime_director
scaffold_hash: c75d0199da0d6146
season: 2
seeds: []
status: complete
tags:
  - skills
  - write
  - mint
  - redesign
thought_session: agi-3a
title: "G7.33.9.1: skills/agi-* on core trunks + .claude/skills symlinks resolve"
town: core
---
# goal:g7.33.9.1

## Why this exists
**Parent `goal:g7.33.9`.** Conjunct 1 of the write/mint foundation: skills must exist on core trunks and `.claude/skills` symlinks must resolve. Measured on tip before this nest (2026-09-28): all 12 `skills/agi-*` dirs present; all 12 `.claude/skills/agi*` symlinks resolve into `skills/`.

## Target end-state
Every `skills/agi-*` directory on core trunks has a `SKILL.md`, and every matching `.claude/skills/<name>` is a symlink whose target resolves under `skills/<name>`.

## Invariants
- symlinks stay relative (`../../skills/...`); never absolute box paths
- skill bodies live only under `skills/`; `.claude/skills` is the harness view

## Falsifier
1. `for d in skills/agi*; do test -f "$d/SKILL.md" || exit 1; n=$(basename "$d"); test -L ".claude/skills/$n" || exit 1; readlink -f ".claude/skills/$n" | grep -q "/skills/$n$"; done` exits 0
2. Negative: any `.claude/skills/agi*` that is a real directory (not a symlink) or whose target is outside the repo

## Out of scope
- skill content quality / director adoption (goal:g7.33.9.2+)
- write.py ergonomics (goal:g7.33.1)

## Agent Notes
Assigned to **belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
skills falsifier green 2026-09-28: all 12 skills/agi* have SKILL.md; all 12 .claude/skills/agi* symlinks resolve under skills/ (NO-PI Belam self-work)
<!-- THOUGHT:END -->
