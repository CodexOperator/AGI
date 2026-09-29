---
id: goal:g7.31.3.3.4
mint_id: 43c0d95304294e3e8180b6cf4c5dacb7
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.31.3.3.4
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e93490e3c351ebce
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
  - core-built-not-wired
title: "G7.31.3.3.4: Refusal writes named row + one send-reply to requesting post -- built on core, NOT wired here (assigned: director-general-1)"
town: core
---
# goal:g7.31.3.3.4

## Why this exists
goal:g7.31.3.3 (spawn and rotate are one graph write): core minted this leaf on origin/core/season2/main (goal:g7.31.3.3.4 there, "Refusal writes named row + one send-reply to requesting post") and marks it complete. Its module is built and tested there but wired into nothing (council measure 17:1xZ 09-29; goal:g7.16.1.3 row S2). It lands here ACTIVE, so no successor reads core's COMPLETE as done.

## Target end-state
- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as extensions/agi/bin/spawn_refusal.py (151 lines), test test_spawn_refusal.py (pass count: the S2 verdict records it), NOT wired into heal/rotate.
- A spawn refusal writes a named row and sends ONE reply to the requesting post.

## Invariants
- Nothing is written on core. A port here names core module + sha in its build node.

## Falsifier
1. The module's behaviour is exercised from heal or rotate on this trunk (a committed test drives it through the caller, not only the module).
2. Negative: until then this leaf reads `status: active`.

## Out of scope
goal:g7.16.1.3 (bundle 3 records the status only; the wiring is not in that bundle)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
mint_id 0ecebfff496a4f25b4f87fc36c54f91d -> 43c0d95304294e3e8180b6cf4c5dacb7 (the Prime's [decision] (a) on sanctuary-master mur wf_67ad5686-154 residue 75, landed by director-general-3): core minted this leaf 09-28 22:43Z as 43c0d95304294e3e8180b6cf4c5dacb7; the trunk re-minted it 09-29 17:53Z under the SAME address, and no node references the trunk id -- so this RESTORES the node's identity, it does not change it (one address, one mint id across towns; the core -> trunk merge no longer forks grid history). The trunk grid ref of 0ecebfff496a4f25b4f87fc36c54f91d is kept. The mint_id line is the only frontmatter change (write.py has no mint_id verb, by design); this THOUGHT is written after it, so the write log holds the final bytes. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
