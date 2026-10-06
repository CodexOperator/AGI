---
id: goal:g4.18.7.3
mint_id: 6e2e491c2ccc430d87163ff977d22ba5
type: goal
parents:
  - goal:g4.18.7
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G4.18.7.3
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 13b6ab7a4c380a27
season: 2
seeds: []
status: retired
tags:
  - council-loop
  - bundle-4
  - local-maxxing
title: "G4.18.7.3: read leaves write.py in ONE cut -- read leaves VERBS in the same row that repoints every teaching site, CLAUDE.md's goal-read line and W-G's reader lines; no alias, never two read paths (row W3c; assigned: director-general-1)"
town: core
---
# goal:g4.18.7.3

## Why this exists
goal:g4.18.7 bullets 1 and 3. Measured 20:3xZ 09-29 at ddea3a61f (the bundle's SM-clean base): VERBS still holds "read" (write.py:543); `viewport.py` has --anchor, --emit human|llm|both and --verify, no single-node body render; grep_live and parked_carriers live in rotation_record.py (:49, :77), imported by write.py:2353 to unpark; the literal teaching form `write.py <id> 'read body|payload` sits in 8 files / 13 lines (10 files on a broader 'read body' grep), the count goal:g4.18.7 now carries (a5848c5a2; its earlier 23 counted a wider scope incl. tests). The row's first act re-measures the teaching sites (the literal regex and the broader grep) and lists them on the hypothesis.

## Target end-state
- "read" is gone from VERBS (write.py:543, :560, :598); a write prints only its own diff. Measured by verdict:dg2b4-w3c: 17 teacher lines in 9 files (the literal grep misses 4) + 2 machine consumers (rotate.py:13702, .geometry/commands.md:911-924), all in this ONE row; the ceiling is raised to 125 (measured 122, min 116), never split (a split is a window with two read paths).
- In the SAME row every teaching site (the agi-node-write skill grammar, CLAUDE.md's 'Read YOUR goal by id' line, QUICKSTART.md, the other skills, W-G's reader lines from goal:g7.16.1.4.1) names the render read from goal:g4.18.7.1.

## Invariants
- There is never a window with two read paths, and never an alias.

## Falsifier
1. `git grep -n '"read":' -- extensions/agi/bin/write.py` prints 0 hits.
2. Negative: `git grep -n -E "write\.py [^ ]+ '?read (body|payload)" -- skills extensions/agi/bin CLAUDE.md QUICKSTART.md extensions/agi/workflows .agi/nodes/.geometry .agi/context/schemas` prints 0 hits.

## Out of scope
goal:g7.16.1.4.1 (lands first and points at today's read)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 4, stage 1, 20:3xZ 09-29) from goal:g4.18.7. Measured 8 files / 13 lines on the literal form versus the goal's 23, so the cut starts by re-measuring rather than inheriting a number. Hypothesis: read-leaves-write-py-with-every-teacher-in-one-row.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
