---
id: goal:g7.16.1.2.2
mint_id: d7b78ea27c4448628c44f529b6218c82
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.2.2
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 895db5466e10e886
season: 2
seeds: []
status: active
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
Residue 41 of sanctuary-master mur wf_dde8f806-ce2 (bundle 2, fixed by director-general-1): Falsifier 1 grepped 'parking test' case-sensitively, but the rule on goal:g7.16.1.1.2 labels it PARKING TEST, so a correct rule printed 0. The grep is now case-insensitive (-ci); the rule's label is unchanged. Mint record: grid history.
<!-- THOUGHT:END -->
