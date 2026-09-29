---
id: goal:g7.31.3.3.3
mint_id: 0d858dc22a26462bbf73f7887d5e2701
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.31.3.3.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 0501fc7405ed37c3
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
  - core-built-not-wired
title: "G7.31.3.3.3: AGI_BOX host-only loop acts and clears needs-rotate -- built on core, NOT wired here (assigned: director-general-1)"
town: core
---
# goal:g7.31.3.3.3

## Why this exists
goal:g7.31.3.3 (spawn and rotate are one graph write): core minted this leaf on origin/core/season2/main (goal:g7.31.3.3.3 there, "AGI_BOX host-only loop acts and clears needs-rotate") and marks it complete. Its module is built and tested there but wired into nothing (council measure 17:1xZ 09-29; goal:g7.16.1.3 row S2). It lands here ACTIVE, so no successor reads core's COMPLETE as done.

## Target end-state
- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as extensions/agi/bin/needs_rotate.py (158 lines), test test_needs_rotate.py (pass count: the S2 verdict records it), NOT wired into heal/rotate.
- The AGI_BOX host-only loop acts on needs-rotate and clears it.

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
mint_id 728af391452a48099416304c3041dce7 -> 0d858dc22a26462bbf73f7887d5e2701 (the Prime's [decision] (a) on sanctuary-master mur wf_67ad5686-154 residue 75, landed by director-general-3): core minted this leaf 09-28 22:43Z as 0d858dc22a26462bbf73f7887d5e2701; the trunk re-minted it 09-29 17:53Z under the SAME address, and no node references the trunk id -- so this RESTORES the node's identity, it does not change it (one address, one mint id across towns; the core -> trunk merge no longer forks grid history). The trunk grid ref of 728af391452a48099416304c3041dce7 is kept. The mint_id line is the only frontmatter change (write.py has no mint_id verb, by design); this THOUGHT is written after it, so the write log holds the final bytes. Prior THOUGHT: grid history.
<!-- THOUGHT:END -->
