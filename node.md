---
id: goal:g7.33.9
mint_id: 65a8f6499c454efbb841185fcc92bfad
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.85
edited_by: belam
goal_id: G7.33.9
goal_kind: subgoal
heading_level: 4
location: source_root
origin: goals-doc
scaffold_hash: c48a5a8b2feef73e
season: 2
seeds:
  - goal:g7.33.9.1
  - goal:g7.33.9.2
status: active
tags:
  - skills
  - write
  - mint
  - redesign
thought_session: belam-sot-land-20260928
title: "G7.33.9: skills + write/mint foundation (redesign order step 1-2)"
town: core
---
<!-- BODY:BEGIN -->
# goal:g7.33.9

## Why this exists
**Parent `goal:g7.33`.** Owner redesign land order 2026-09-28: **skills → write/mint → spawn/rotate → messaging**. SoT (`doc:belam-grok-internals`) already refs skill:agi-node-write · agi-goal · … Directors+Belam pursue write/mint via skills under NO-PI HARD (owner FULL STOP), not inlined PROFILE. This leaf is the adoption/order track; G7.33.1 remains the engine FIX track for write.py ergonomics.

## Target end-state
| # | conjunct |
|---|---|
| 1 | `skills/agi-*` present on core trunks and `.claude/skills` symlinks resolve to them |
| 2 | every node+goal write by Belam/directors goes through write.py + skill:agi-node-write / skill:agi-goal (no hand-edit of `.agi/nodes`) |
| 3 | write/mint foundation residues that block clean adoption are nested under this leaf (or under G7.33.10) as bare-active self-work leaves — never left as card prose |

## Invariants
- skill files are the procedures; SoT carries skill *refs*, never pasted skill bodies
- G7.33.1 hypotheses stay the write.py ergonomics FIX track; this leaf does not re-own them
- NO-PI: complete via self-work / non-pi only until owner lifts

## Falsifier
1. `test -f skills/agi-node-write/SKILL.md && test -L .claude/skills/agi-node-write && readlink -f .claude/skills/agi-node-write | grep -q skills/agi-node-write` exits 0 for every skills/agi-* (positive)
2. Negative: a committed edit under `.agi/nodes/` that bypasses write.py (no write-log actor row for that path in the same commit window) — forbidden while this leaf is active

## Out of scope
- goal:g7.33.1 write.py ergonomics FIX rounds (a/b/c)
- goal:g7.31.6 spawn/rotate via skills (redesign step 3; horizon)
- goal:g7.32.5 messaging/magic-pane (redesign step 4; horizon)

## Agent Notes
Assigned to **belam** (Prime tree-build under NO-PI). Directors self-work nested leaves; no director pings unless blocker.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
deepened under NO-PI: filled bare body; nested .1 (skills present→COMPLETE) + .2 (title regex residue of .10→COMPLETE code+tests); parent stays active for conjunct 2 (directors write via skills) + further write/mint residues
<!-- THOUGHT:END -->
