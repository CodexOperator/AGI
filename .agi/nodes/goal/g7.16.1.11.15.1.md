---
id: goal:g7.16.1.11.15.1
mint_id: 3f73b949c25b4add8a5a8f5bf0a163ae
type: goal
key: 664244b07d7040d2
parents:
  - goal:g7.16.1.11.15
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.11.15.1
goal_kind: subgoal
origin: goal
season: 2
seeds:
  - goal:g7.16.1.11.15
status: horizon
tags:
  - council
  - phase-w
  - g7.16.1.11.15
title: "G7.16.1.11.15.1: PHASE W -- MOVE workflow.py + workflow_note.py never git rm; RENAME skill agi-workflow to agi-spawn-chain; KEEP 16 json live"
town: core
---
# goal:g7.16.1.11.15.1

## Why this exists
goal:g7.16.1.11.15 (Z4 ladder out, PHASE W): SM [coord] 20:48Z 10-05 placed this nested leaf from hypothesis:aio-w-and-mail-one-living-path (AIO, trunk 703e7ad58). Parent measured: workflow.py retires as ONE round; skill RENAME to agi-spawn-chain (owner 17:4xZ). AIO CLAIM: 16 json KEEP live; workflow.py 159516 + workflow_note 7682 MOVE (deprecate+move, never git rm). AIO v3 + SM 20:56Z: KEEP 30, js frozen (never executed, never updated).

## Target end-state
- workflow.py and hooks/workflow_note.py: status deprecated + moved, never `git rm`.
- Skill agi-workflow RENAME agi-spawn-chain; re-point skills agi, agi-corrective, agi-master-gate, agi-merge-pass, agi-dispatch + rotations facts F29/F5. Prime: ONE rotations skills-clause rename (pb3).
- 16 json manifests in extensions/agi/workflows/ KEEP live.
- 14 js KEEP live and frozen (never executed, never updated). AIO v3 / SM 20:56Z. Not MOVE with the py.
- config:commands `workflow:` tag KEEP (not the py). `workflow.py:*` cells MOVE with the py.
- A v4 post's review is a SPAWN (manifest + graph slice + agi-kid -m), never shells workflow.py.

## Invariants
- Nothing is deleted. Sum of live + deprecated files never drops.
- 0 B in the zygote. No implement on this mint (SM: No implement yourself).
- KEEP 30 (16 json + 14 js frozen). Owner/AIO v3, not this seat's pick.

## Falsifier
1. `git ls-files -- extensions/agi/bin/workflow.py extensions/agi/hooks/workflow_note.py` prints 0 live paths AND the files exist under `.agi/nodes/deprecated/` or the retired sibling; `test -d skills/agi-spawn-chain` exits 0; `git grep -l workflow.py -- skills/agi/SKILL.md skills/agi-corrective skills/agi-master-gate skills/agi-merge-pass skills/agi-dispatch` prints 0.
2. Negative: `git log --diff-filter=D --name-only -- extensions/agi/bin/workflow.py extensions/agi/workflows/*.js` prints 0 paths (never git rm).

## Out of scope
goal:g7.16.1.11.11.2 (AA1 box KEEP; send.py MOVE) · Prime rotations sub · agi-infer · season.py rollover --apply

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
20:57Z 10-05 (date -u): SM [coord] 11.15.1 KEEP 30 js frozen (AIO v3). Chew only. No implement. No push.
<!-- THOUGHT:END -->
