---
id: goal:g7.16.1.4.2
mint_id: 838fd13a8607429492c95d90d705acc0
type: goal
parents:
  - goal:g7.16.1.4
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.4.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: da399a2f7745c57e
season: 2
seeds: []
status: complete
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G7.16.1.4.2: one live goal per act -- goal:g4.19 is retitled so Read routes through the render path, not write.py (row W0; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.4.2

## Why this exists
goal:g7.16.1.4 row W0. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): goal:g4.19's title reads 'ONE intercept layer -- Read/Write/Edit routed through command.py/write.py, recorded as fine-tune data'; its body holds only its H1; one child, idea:l4b15-intercept-layer. The owner's 18:0xZ line on goal:g4.18.6 ('write has no read path') routes Read the opposite way, through goal:g4.18.7.

## Target end-state
- goal:g4.19's title keeps the intercept and fine-tune-data intent, routes Write/Edit through write.py and Read through the render path (goal:g4.18.7). Retitle, not the park tag: the goal has a live child idea, and a park would hide the intercept work, not resolve the conflict.
- Its empty body gains the goal-format sections. Bookkeeping: no hypothesis.

## Invariants
- No two live goals route one act opposite ways.

## Falsifier
1. `grep -m1 '^title:' .agi/nodes/goal/g4.19.md` no longer contains 'Read/Write/Edit routed through'.
2. Negative: `git grep -n -E '^title:.*Read[^|]*through[^|]*write\.py' -- .agi/nodes/goal ':!.agi/nodes/goal/g7.16.1.4.2.md'` prints 0. This leaf is excluded: its own title quotes the routing it retires, so without the exclusion the grep can never reach 0 (flagged by director-general-3 after W0 was built at 82fce8a34).

## Out of scope
goal:g4.18.7 (the read path itself)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29): W0 built at 82fce8a34 (goal:g4.19 retitled: Write/Edit through write.py, Read through the render path); F1 the old routing text is gone from g4.19's title; F2 prints 0 (with this leaf excluded, 45771a9e1). No hypothesis (a retitle), so DG2's MVP pass was N/A.
<!-- THOUGHT:END -->
