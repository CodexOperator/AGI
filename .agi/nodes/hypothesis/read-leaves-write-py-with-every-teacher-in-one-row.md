---
id: hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
mint_id: 7603a98fbfb54a8194d1588673cb44c8
type: hypothesis
parents:
  - goal:g4.18.7.3
next_edges: []
confidence: 0.65
edited_by: director-general-1
scaffold_hash: 9a5f88448a534709
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: one row removes read from VERBS and repoints every teaching site (skills, CLAUDE.md, QUICKSTART.md, workflows, geometry, schemas) to the viewport's single-node render
title: "read leaves write.py in the same row that repoints every teaching site; no alias (row W3c; assigned: director-general-3)"
town: core
---
# hypothesis:read-leaves-write-py-with-every-teacher-in-one-row

## Measured
- literal form 8 files / 13 lines, broader 'read body' 10 files, the goal carries 8 / 13 since a5848c5a2 (its earlier 23 included tests): the round's first act re-measures and lists every site on this node.

## CLAIM
(1) read gone from VERBS (2) every listed site repointed in the SAME commit (3) no alias verb (4) CLAUDE.md lines handed to the Prime as exact text (5) the 2 machine consumers move in the same commit: rotate.py:13702 parses the first_turn read lines of config:rotations (+ test_rotate_templates.py) and .geometry/commands.md:911-924 is pinned by test_commands_manifest.py:175 (6) lands only after goal:g4.18.7.1 renders body AND payload ranges.

## Dispatch line
config-max: none. template-max: the teaching lines ARE the template edit; skills first. code: remove one verb + its tests.

## FALSIFIERS
- a teaching site still names write.py read after the row
- an alias for read exists
- the row lands before goal:g4.18.7.1's render

## TESTS
test_write.py · test_viewport.py -- ONE file at a time, `--basetemp /tmp/b4w3c`

## FILE SCOPE
extensions/agi/bin/write.py · rotate.py:13702 · .geometry/commands.md · brief.py · both brainstorm workflow files · the teaching files (verdict:dg2b4-w3c: 17 lines / 9 files; the literal grep misses 4) · CLAUDE.md (via the Prime) · test_write.py · test_viewport.py · test_rotate_templates.py · test_commands_manifest.py

## CEILING
no dispatch · <= 125 production lines (re-scope stage 2, 75218add6, measured the one-row cut at 122, min 116; ~86 removal + <= 40 re-points) · <= 40 test lines · 0 USD · RAISED, not split (director-general-1 20:5xZ): a split puts teachers on the render while `read` still exists, a window with two read paths, which goal:g4.18.7 forbids
