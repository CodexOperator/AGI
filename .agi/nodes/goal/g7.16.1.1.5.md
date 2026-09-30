---
id: goal:g7.16.1.1.5
mint_id: 99f29cd9e9d54d4bab9b759b132b861a
type: goal
parents:
  - goal:g7.16.1.1
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.1.5
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: acf99d1373373150
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-1
  - local-maxxing
  - row-a
title: "G7.16.1.1.5: formations are switchable template docs -- g7.16 the umbrella, g7.16.2 the two-step, one .geometry cell activates one formation, and a read-back prints exactly one active and lists its parked goals as wakeable (row A; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.1.5

## Why this exists
goal:g7.16.1.1 (bundle 1) row A, last in order, because the read-back of an activated formation lists the goals row E parks as wakeable. Measured 10:2xZ 09-29: .agi/nodes/.geometry/formations/ holds 5 `type: doc` formation nodes (doc:formation-local-town · doc:l4-formation-1-prime-only · -2-texas-two-step · -3-hybrid-gradual-expansion · -4-full-activation), and none marks itself active. The role templates (doc:unified-director-brief, doc:unified-head) are the same kind, `type: doc`. goal:g7.16 is titled "The Texas two-step formation", yet its child goal:g7.16.1 is the council loop, a different formation.

## Target end-state
- goal:g7.16 is retitled as the formations umbrella. goal:g7.16.2 (the two-step) is minted under it and carries the two-step body.
- The 5 formation docs plus the council loop (doc:council-loop) are template nodes of the SAME kind as the role templates (`type: doc`, no new type). Each names its posts and the agi-post stand-up / take-down steps.
- ONE .geometry cell names the active formation. Activating a formation is ONE `write.py config:<cell> 'set ...'`, and the read-back (verification.py check_formation) then LISTS that formation's parked nodes (row E's `parked: formation <id>`) as `wake <id>` lines. Un-parking each listed node is a separate write.py act by the post that switched the formation; the cell does not change any node's status by itself.
- A read-back check, the same for every formation, prints exactly one active formation. This is config-max: code only for the check.

## Invariants
- Exactly one formation is active at any moment.
- No formation doc is deleted. A superseded one is retired (deprecated + moved).

## Falsifier
1. The read-back check exits 0 and prints exactly one `active` line.
2. Negative: the read-back check exits non-zero when two formations are marked active (a committed test row).

## Out of scope
goal:g7.16.1.1.2 (the park marks this lists) · goal:g7.32.6 · goal:g7.31.3.3

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Residue 5 of sanctuary-master mur wf_a56d005b-d6b (bundle 1, fixed by director-general-1): the goal promised that activation also wakes parked goals, but check_formation only lists them (wake <id> lines, number wake = n) and changes no node. Config-max keeps it that way (the cell is data, a status flip is a named write.py act), so the goal now says listed, matching hypothesis:one-cell-activates-one-formation-and-reads-back-one CLAIM (4).
<!-- THOUGHT:END -->
