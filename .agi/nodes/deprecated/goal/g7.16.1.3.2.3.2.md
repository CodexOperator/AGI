---
id: goal:g7.16.1.3.2.3.2
mint_id: 9bf47938d3684f49a1950407c7fcf128
type: goal
parents:
  - goal:g7.16.1.3.2.3
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.2.3.2
goal_kind: subgoal
heading_level: 7
origin: goals-doc
scaffold_hash: dfd28679788d4a77
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-h4
title: "G7.16.1.3.2.3.2: the formation gate never fails open -- _grep_live FAILs on a git-grep error and names a malformed-frontmatter hit instead of raising (mur residue f; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.2.3.2

## Why this exists
goal:g7.16.1.3.2.3, residue (f) of council mur wf_4e0708df-4ef: verification.py `_grep_live` runs `git grep` (verification.py:1290) and ignores its exit code, so a git error reads as "no hits" and the park/formation gate FAILS OPEN. The same reader calls `yaml.safe_load` on each hit's frontmatter (:1296), which raises on a malformed hit instead of reporting it.

## Target end-state
- FIRST in H4 (council add 1, c0c8d3f82). `_grep_live` fails CLOSED: `git grep` exit 1 = no hits; exit >= 2 = a FAIL carrying the error line.
- A hit whose frontmatter does not load is reported by name (a FAIL row), never an uncaught exception.

## Invariants
- The live graph still PASSes the formation check.

## Falsifier
1. A committed test: a git-grep error (e.g. a bad pathspec in a tmp repo) makes the check FAIL, and a malformed-frontmatter fixture is named in the FAIL note.
2. Negative: `_grep_live` has no path that discards a non-0/1 returncode.

## Out of scope
goal:g7.16.1.3.2.1 (moving parked_carriers into the shared module; this fix rides wherever the function lives)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by director-general-1 (23:4xZ 09-29) under the owner's 23:5xZ loop (build vs goal, then outcome); bundle 3 SM mur CLEAN at 1f39ffb1c covers the test halves. F2: grep_live handles git grep's returncode (2 sites); F1 test built with mvp:dg3-h4f-grep-fails-closed.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
