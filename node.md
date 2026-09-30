---
id: goal:g4.19
mint_id: 9ce60ef0585b4565a6d0480c2134b35e
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G4.19
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 1ba788b8d26d82ea
season: 2
seeds:
  - idea:l4b15-intercept-layer
  - hypothesis:l4b15-intercept-layer
status: active
tags:
  - goal
  - subgoal
thought_session: g1-g7-rewrite-2026-09-19
title: "G4.19: ONE intercept layer — Write/Edit through write.py, Read through the render path (goal:g4.18.7), every act recorded as fine-tune data"
---
<!-- BODY:BEGIN -->
# goal:g4.19

## OWNER 2026-09-29 18:0xZ, verbatim (Prime pane, relayed by belam-S2-L5-XVI to the council; copied from goal:g7.16.1.4)
"Write shouldn't need a read path. We should only need a render path. Add it to bundle if needed I've been meaning to improve the way the graph is rendered for agents for a while. Unify everything into the correct slots. Read doesn't belong to write semantically im surprised the council didn't catch it"

## Why this exists
goal:g4 (the engine's own tooling) is its parent: every agent Read/Write/Edit on a node went around the engine, so no act was recorded and no edit was gated. The intercept records each act as fine-tune data. Until 2026-09-29 the title routed Read through write.py as well; the owner's 18:0xZ line above sends Read the other way (goal:g4.18.7), and goal:g7.16.1.4 row W0 (goal:g7.16.1.4.2) retitled this goal so that no two live goals route one act in opposite directions.

## Target end-state
- ONE intercept layer sees every agent act on a node and records it as fine-tune data.
- Write and Edit reach a node only through write.py (the one writer, its authorship gate).
- Read reaches a node only through the render path of goal:g4.18.7; the intercept records the read and never routes it through write.py.

## Invariants
- No two live goals route one act in opposite directions (goal:g7.16.1.4.2).
- write.py never gains a read path (owner 18:0xZ above).

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_intercept_layer.py -q` exits 0: the committed test drives one Read, one Write and one Edit through the intercept and finds exactly one fine-tune record per act, the Read taken from the render path (goal:g4.18.7) and the Write/Edit from write.py. The file does not exist yet, so this stays red until the intercept is built (its hypothesis goes under idea:l4b15-intercept-layer).
2. Negative: `grep -cE '^title:.*Read[^|]*through[^|]*write\.py' .agi/nodes/goal/g4.19.md` prints 0 (anchored on this node alone, so goal:g7.16.1.4.2's "not write.py" title cannot match).

## Out of scope
goal:g4.18.7 (the read path itself) · goal:g4.18.5 (rows, and a write is a commit)

## Agent Notes
Assigned to **none**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
W0 (goal:g7.16.1.4.2, council bundle 4, director-general-3): retitled under the owner 18:0xZ line (write has no read path). The old title routed Read/Write/Edit through command.py/write.py, the opposite of goal:g4.18.7. Retitled rather than parked because idea:l4b15-intercept-layer is a live child and a park would hide the intercept intent. This version closes SM residues 84-85 (wf_55fc5dde-0e5): the negative falsifier is anchored on this file alone (the old tree-wide grep matched goal:g7.16.1.4.2 and printed 1), the falsifiers are exit-code CLIs on this goal own end-state, and Agent Notes carries its Assigned line.
<!-- THOUGHT:END -->
