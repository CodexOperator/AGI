---
id: goal:g7.16.1.1.2
mint_id: ced616e5c90c462581caa9f5d8e94d7a
type: goal
parents:
  - goal:g7.16.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.1.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: d25ae0c0b4c0e661
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-1
  - local-maxxing
  - row-e
title: "G7.16.1.1.2: every residue row under g1.26-g1.29 and g7.33.19 carries one mark -- keep, park (horizon, parked: formation g7.16.2), retired, or pointer to one core g7.33 leaf; g7.32.5 parked (row E; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.1.2

## Why this exists
goal:g7.16.1.1 (bundle 1) row E: the residue goals goal:g1.26 · g1.27 · g1.28 · g1.29 · g7.33.19 were written for the dispatch formation, which is off (goal:g7.16.1: no parent/kid dispatch). Measured 10:2xZ 09-29: 21 live hypotheses sit under g1.26-g1.29 (9 · 5 · 6 · 1 parent edges; four are residue-batch nodes holding their own rows), g7.33.19 holds 26 table rows and 6 child nodes, and goal:g7.32.5 has 0 children. Each of these goals has at most one THOUGHT pair, at column 0, so the goal-level writes here cannot trip row B's bug. The council ordered B before E because the thought verb can rewrite a quoted pair. Measured 10:4xZ: all 27 nodes carrying a g1.26-g1.29 / g7.33.19 parent edge hold at most one THOUGHT pair, at column 0, with no indented or quoted pair, so row E does not wait on B landing.

## Target end-state
- Every row carries exactly one mark, by THE TRIAGE RULE (the one rule every triage THOUGHT cites): **keep** = a live defect in machinery every formation runs (write.py, rotate, heal, the suite, the mur engine) or a false verdict on the graph; worked as a leaf in this loop · **park** = lives only in dispatch, round, kid, spawn or provisioning machinery, or in a round's own record text; marked by the THOUGHT line `parked: formation g7.16.2` and, on a GOAL, also `status: horizon` (a hypothesis has no status field in [hypothesis].md, so its THOUGHT line alone is the mark); it wakes when that formation is active again · **retired** = no work left under ANY formation: either wrong under every formation, or its residue already fixed, and the THOUGHT names the measure (the fixing commit or the green test); this is the row mark, distinct from a goal's `complete` · **pointer** = a duplicate of a core g7.33.* leaf: points at that ONE leaf, no twin.
- goal:g7.32.5 (parents send on the hub route) is parked, not retired.
- Split one leaf per source so each closes on its own: goal:g7.16.1.1.2.1 (g1.26-g1.29) · goal:g7.16.1.1.2.2 (g7.33.19 + g7.32.5).

## Invariants
- Nothing is deleted. A parked GOAL is `status: horizon`, since `held` is not a legal status ([goal].md); a parked hypothesis carries the THOUGHT mark only. A retire carries its measured reason in THOUGHT.
- Every pointer names exactly one target leaf.

## Falsifier
1. Every leaf under this one reads `status: complete`: `git grep -h '^status:' -- .agi/nodes/goal/g7.16.1.1.2.*.md | sort | uniq -c` prints only `complete`.
2. Negative: rows under g1.26-g1.29 / g7.33.19 without a keep|park|retired|pointer mark = 0 (counted by each sub-leaf's own falsifier).

## Out of scope
goal:g7.32.6 · goal:g7.31.3.3 (the messaging and spawn/rotate redesigns: after bundle 2) · the DE pi-lane queue (EG.185, EG.211-226)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residues 3 + 4 of sanctuary-master mur wf_a56d005b-d6b (bundle 1, fixed by director-general-1). (3) 27 triage THOUGHTs cited the rule on goal:g7.16.1.1.2, but the rule they applied (director-general-2) was on no node, and their retired = no residue left contradicted wrong under EVERY formation; THE TRIAGE RULE now sits in Target end-state, word for word the one applied, and retired is defined as no work left under any formation (wrong everywhere OR fixed, measure named), which keeps the mark set at four so every falsifier grep still holds. (4) park = status horizon could not bind 14 parked hypotheses ([hypothesis].md has no status field): a goal parks by status + THOUGHT, a hypothesis by the THOUGHT line alone. Prior version (E need not wait on B, measured on 27 nodes): grid history.
<!-- THOUGHT:END -->
