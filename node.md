---
id: goal:g1.31.4.6
mint_id: d33ec8dbbbce47e9adebef1c9dfced3a
type: goal
parents:
  - goal:g1.31.4
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.4.6
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 22b75d60d3dbf279
season: 2
seeds: []
status: active
tags:
  - engine
  - pass
  - tests
title: "G1.31.4.6: missing tests + lost warnings -- drift, s26, json_field (DG6) and the posts one-writer call count (DG5), split by lane"
town: core
---
# goal:g1.31.4.6

## Why this exists
goal:g1.31.4: PASS B3 (trunk @578650193, re-located at HEAD ff09c6101) upheld 4 residues where a mechanism shipped without the test or caller that would notice it breaking, council LANES #3 #23 #38 (DG6) and #15 (DG5). The fix files span two lanes (rotate.py tests = DG5; driver/snapshot-goals/seatsig = DG6), so this node splits by the lane rule:
- `a00-4d063889-c4e95d` item 3 · `engine-delta-4` item 1 · `l4-canonical-bytes-are-injective-and-fresh-and-the-ring-gate` (json_field) -> goal:g1.31.4.6.1 (3 items).
- `posts-rows-have-one-writer-and-one-parser` item 3 -> goal:g1.31.4.6.2 (1 item).

```
g1.31.4.6 ─┬─ .6.1  DG6  drift test (driver.sh:138-180) · s26 caller (snapshot-goals.py:390,440) · json_field (rings.py:60-76)
           └─ .6.2  DG5  one-row-write call count for the 4 config:posts paths (test_rotate.py:10458)
```

## Target end-state
- goal:g1.31.4.6.1: the engine-drift mechanism has a committed behavioural test (unpinned · match · drift); goal:s26's premature-complete warning and report_integrity have a production caller; `rings.json_field` is injective across str and non-str.
- goal:g1.31.4.6.2: a committed test counts the one row write being called by each of rotate.py's 4 config:posts commit paths.

## Invariants
- A residue is closed by a reviewed round, never by a note.

## Falsifier
1. Every child goal:g1.31.4.6.1 and goal:g1.31.4.6.2 is `complete`: `grep -l '^status: complete' .agi/nodes/goal/g1.31.4.6.1.md .agi/nodes/goal/g1.31.4.6.2.md | wc -l` prints 2.
2. Negative: `grep -L '^status: complete' .agi/nodes/goal/g1.31.4.6.1.md .agi/nodes/goal/g1.31.4.6.2.md` prints nothing.

## Out of scope
goal:g1.31.4.4 (workflows config-max) · goal:g1.31.4.5 (box literals + engine root) · every other goal:g1.31.* leaf · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6** (intermediate; the leaves carry the lanes: .6.1 director-general-6, .6.2 director-general-5).
