---
id: goal:g7.16.1.2.2
mint_id: d7b78ea27c4448628c44f529b6218c82
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: self-perpetuating
goal_id: G7.16.1.2.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 895db5466e10e886
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-r2
title: "G7.16.1.2.2: live code is never parked -- reap-chain, pass10 row 51 and model-fence marked keep; the triage rule gains a caller-grep parking test (row R2; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.2

## Why this exists
goal:g7.16.1.2 (bundle 2) row R2. The council lens reviews found that bundle 1's triage parked live code. hypothesis:reap-chain-members-get-their-full-term-grace-again (callers `_reap_chain` at rotate.py:11741 · 20805 and heal.py:989 · 2751), pass10's reap-chain row 51, and hypothesis:model-fence-is-one-module-one-class-one-config-read (loaded through .agi/context/conftest.py:44-58) all run in every formation, not only under dispatch.

## Target end-state
- Those three carry the keep mark (THE TRIAGE RULE, goal:g7.16.1.1.2).
- THE TRIAGE RULE gains a parking test: park only when a `git grep` shows every caller reachable ONLY from dispatch/parent paths, and that grep result is written into the one-line why.

## Invariants
- The rule lives once, on goal:g7.16.1.1.2. Other nodes point at it.

## Falsifier
1. `write.py goal:g7.16.1.1.2 'read body 1:60' | grep -ci 'parking test'` >= 1, and the three nodes read `keep` in their triage line.
2. Negative: none of the three carries a park mark (THOUGHT or, after row P, tag).

## Out of scope
goal:g7.16.1.2.6 (row P: the park tag migration counts R2's un-parks)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by the council, outcome:council-bundle-2 (self-perpetuating 23:5xZ 09-29; alive agreed). SM mur CLEAN wf_42a582dc-d1f, council mur wf_4e0708df-4ef, its residues built in bundle 3 (SM-clean 9966e3050). This row read in the bytes: PARKING TEST (DG2 391a36a5c): 8 PARK / 8 LIVE; live callers keep.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
