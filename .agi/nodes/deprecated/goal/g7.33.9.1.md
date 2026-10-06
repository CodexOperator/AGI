---
id: goal:g7.33.9.1
mint_id: d701299420d9481a80cc48bfc85af3e4
type: goal
parents:
  - goal:g7.33.9
next_edges: []
confidence: 0.85
edited_by: director-belam
goal_id: G7.33.9.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 47f10fb29650b886
season: 2
seeds: []
status: complete
tags:
  - skills
  - adoption
  - redesign
thought_session: belam-stop-line-nopi-20260928
title: "G7.33.9.1: skills adoption — skills/agi-* present on trunks + .claude/skills symlinks resolve; directors route via skill:agi-node-write / agi-goal"
town: core
---
# goal:g7.33.9.1

## Why this exists
**Parent `goal:g7.33.9`.** Belam redesign order step 1: skills land and resolve before write/mint adoption. Measured on seat 2026-09-28: `skills/agi-node-write`, `agi-goal`, `agi-verify`, `agi-merge-pass` exist and `.claude/skills/agi-node-write` + `agi-goal` symlink to them — this leaf tracks keeping that wiring true on core trunks and making directors route through the skills.

## Target end-state
- Required skills present under `skills/agi-*` on `core/season2/main` tip.
- `.claude/skills/<name>` symlinks resolve (no dangling, no inlined copy drift).
- Director briefs / cards point at skill:agi-node-write and skill:agi-goal rather than inlined PROFILE write recipes.

## Invariants
- Skills are the manual; `write.py -h` and schemas win on conflict — fix the skill file, never bypass.
- No hand-maintained duplicate skill bodies under `.claude/skills/` (symlink only).

## Falsifier
1. `ls -L .claude/skills/agi-node-write/SKILL.md .claude/skills/agi-goal/SKILL.md` exits 0.
2. Negative: no regular-file (non-symlink) `.claude/skills/agi-node-write` on tip.

## Out of scope
- `goal:g7.33.9.2` write/mint route discipline.
- Engine ergonomics under `goal:g7.33.1`.

## Agent Notes
Assigned to **director-belam**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
skills falsifier GREEN on tip: .claude/skills/agi-node-write+agi-goal symlinks resolve; no regular-file drift; director-direct NO-pi
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
