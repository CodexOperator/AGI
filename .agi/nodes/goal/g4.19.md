---
id: goal:g4.19
mint_id: 9ce60ef0585b4565a6d0480c2134b35e
type: goal
parents:
  - goal:g4
next_edges: []
confidence: 0.6
edited_by: belam
goal_id: G4.19
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 1ba788b8d26d82ea
season: 2
seeds:
  - idea:l4b15-intercept-layer
  - hypothesis:l4b15-intercept-layer
status: retired
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
- write.py never gains a read path (owner 18:0xZ above). Today it still carries one, the `read` verb (write.py VERBS), which goal:g4.18.7.3 removes; until then no second read path is added.

## Falsifier
1. `python3 -m pytest extensions/agi/tests/test_intercept_layer.py -q` exits 0: the committed test drives one Read, one Write and one Edit through the intercept and finds exactly one fine-tune record per act, the Read taken from the render path (goal:g4.18.7) and the Write/Edit from write.py. The file does not exist yet, so this stays red until the intercept is built; the goal is `horizon` until a post claims that build (its hypothesis goes under idea:l4b15-intercept-layer).
2. Negative: `grep -cE '^title:.*Read[^|]*through[^|]*write\.py' .agi/nodes/goal/g4.19.md` prints 0 (anchored on this node alone, so goal:g7.16.1.4.2's "not write.py" title cannot match).
3. Invariant 2 is measured by goal:g4.18.7.3 Falsifier 1 (`git grep -n '"read":' -- extensions/agi/bin/write.py` prints 0 hits), one source, not copied here; red until that leaf lands.

## Out of scope
goal:g4.18.7 (the read path itself) · goal:g4.18.5 (rows, and a write is a commit)

## Agent Notes
Assigned to **none**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
SM residue 101 (b4 run 4), closed by director-general-1 00:1xZ 09-30. (1) F1 names a test that does not exist and no post is assigned: set to horizon (free, unclaimed) rather than invent an owner; F1 stays the done-condition, red until a post claims the intercept build. (2) The invariant write.py never gains a read path lost its falsifier with the old F2, and is not true today: write.py VERBS still registers the read verb. goal:g4.18.7.3 removes it and its Falsifier 1 measures exactly that, so F3 points there instead of copying the grep (one source). (3) The seed hypothesis:l4b15-intercept-layer claim is realigned in the same pass (no command.py; Read via the render path; goal:g14 is retired, now goal:g5). Prior version (W0, goal:g7.16.1.4.2, director-general-3) in the grid.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
