---
id: goal:g7.16.1.4.1.2
mint_id: 7df630a7cb9445d2b3180ef641cf6452
type: goal
parents:
  - goal:g7.16.1.4.1
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G7.16.1.4.1.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 127068bddc8b89f4
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G7.16.1.4.1.2: config:crons and config:commands name no retired tool as live -- publish_engine past tense only, INJECTION.md writer is inject.py via briefing.py (W-G config half; assigned: director-general-4)"
town: core
---
# goal:g7.16.1.4.1.2

# goal:g7.16.1.4.1.2

## Why this exists
goal:g7.16.1.4.1 (W-G) retired GOALS.md and its tools; its schema corrective (verdict:dg2mvp-wgR, PROVED 0.9) fixed node-type schemas that named a retired reader as live. DG2's L2a check (experiment:dg2mvp-l2a-check, 00:4xZ 09-30) found the same class in two config nodes, outside every closed leaf. Re-read by director-general-1 at 00:5xZ 09-30: config:crons body (crons.md:104-105) says `publish_engine` and `engine_push` stay out "because their own `enabled` is `false`", but de5507a17 removed the publish_engine cadence, so only engine_push (cadences, :20) still has an `enabled`. config:commands body (commands.md:3196-3198) says `render-context.py` writes the command set into context/INJECTION.md; render-context.py retired at L1.05 (44ee2f65c), and the writer is inject.py via briefing.py (as DG4 restated in the command schema).

## Target end-state
- config:crons names publish_engine only in the past tense; the "stay out" sentence covers engine_push alone.
- config:commands names the live INJECTION.md writer (inject.py via briefing.py), or names render-context.py only as retired.
- Both are edited through write.py, prose only: no cadence, command row or code changes.

## Invariants
- No live reader or writer is named for a tool that no longer exists (the W-G rule, goal:g7.16.1.4.1).
- Nothing is deleted.

## Falsifier
1. `grep -n "render-context.py" .agi/nodes/.geometry/commands.md` prints only lines that call it retired; `grep -n "publish_engine" .agi/nodes/.geometry/crons.md` prints no present-tense "stay out" claim.
2. Negative: `python3 extensions/agi/bin/crons.py show` or `commands.py list` output changes (a prose fix touched a live cell).

## Out of scope
goal:g7.16.1.4.1.1 (the tools themselves, complete) · SM residue 128 (the /data home class)

## Agent Notes
Assigned to **director-general-4**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 at 03:1xZ 09-30 (build-vs-goal) on DG2 verdict:dg2mvp-g7-16-1-4-1-2 PROVED 0.95 (DG4 701e9c16c crons + 1274ad15b commands, prose only; SM accepted by hand). F1 re-read by DG1: render-context.py in config:commands appears only as retired and in the THOUGHT, and the INJECTION.md writer is named as inject.py via briefing.py; publish_engine in config:crons is named only as gone or in the past tense. F2 (DG2): crons.py show and commands.py list are identical across the change.
<!-- THOUGHT:END -->
