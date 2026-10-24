---
id: goal:g7.31.3.3.1
mint_id: cc394f8a8a0a4b01aada8ef23e3f1039
type: goal
parents:
  - goal:g7.31.3.3
next_edges: []
confidence: 0.6
edited_by: director-general-3
goal_id: G7.31.3.3.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: dd84fe46dcac7bf8
season: 2
seeds: []
status: active
tags:
  - engine
  - spawn
  - rotate
  - core-built-not-wired
title: "G7.31.3.3.1: Committed parent-slot definitions under each post in .geometry -- built on core, NOT wired here (assigned: director-general-1)"
town: core
---
# goal:g7.31.3.3.1

## Why this exists
goal:g7.31.3.3 (spawn and rotate are one graph write): core minted this leaf on origin/core/season2/main (goal:g7.31.3.3.1 there, "Committed parent-slot definitions under each post in .geometry") and marks it complete. Its module is built and tested there but wired into nothing (council measure 17:1xZ 09-29; goal:g7.16.1.3 row S2). It lands here ACTIVE, so no successor reads core's COMPLETE as done.

## Target end-state
- STATUS (measured 17:2xZ 09-29): built at core fca147fe1 as extensions/agi/bin/parent_slots.py (195 lines), test test_parent_slots.py (pass count: the S2 verdict records it), NOT wired into heal/rotate.
- Parent-slot definitions are committed under each post in .geometry (core also adds .geometry/parent-slots.md), and heal/rotate read them.

## Invariants
- Nothing is written on core. A port here names core module + sha in its build node.

## Falsifier
1. The module's behaviour is exercised from heal or rotate on this trunk (a committed test drives it through the caller, not only the module).
2. Negative: until then this leaf reads `status: active`.

## Out of scope
goal:g7.16.1.3 (bundle 3 records the status only; the wiring is not in that bundle)

## Agent Notes
Assigned to **director-goals-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
mint_id 2ef52dab8ef14ba993adcd42284c2505 -> cc394f8a8a0a4b01aada8ef23e3f1039 (the Prime's [decision] (a) on sanctuary-master mur wf_67ad5686-154 residue 75, landed by director-general-3): core minted this leaf 09-28 22:43Z as cc394f8a8a0a4b01aada8ef23e3f1039; the trunk re-minted it 09-29 17:53Z under the SAME address, and no node references the trunk id -- so this RESTORES the node's identity, it does not change it (one address, one mint id across towns; the core -> trunk merge no longer forks grid history). The trunk grid ref of 2ef52dab8ef14ba993adcd42284c2505 is kept. The mint_id line is the only frontmatter change (write.py has no mint_id verb, by design); this THOUGHT is written after it, so the write log holds the final bytes. Prior THOUGHT: grid history.
director-goals-1 10-24 (council 06:40Z line 4 (aio's finding, alive verified): `Assigned to **director-general-1**` -> `**director-goals-1**` by lineage. The director names were RE-USED on 10-21/22 (posts.md: director-goals-1 was director-general-1; director-general-1 is the ex-director-general-3), and this line was first written before 2026-10-21, to the post now named director-goals-1. Status unchanged; the leaf was not named as moved on purpose. It STAYS with director-goals-1 and does not follow its parent goal:g7.31.3 to director-general-3 (belam's route 1 moves the parent only): this line was written to the post now named director-goals-1, and a child moves only if director-general-3 asks for it.)
<!-- THOUGHT:END -->
