---
id: goal:g7.16.1.2.1
mint_id: 15ad2bff1cb24573a525a2902565f436
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: self-perpetuating
goal_id: G7.16.1.2.1
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 033c33a370b739d0
season: 2
seeds: []
status: complete
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-r1
title: "G7.16.1.2.1: rotation records carry ~-relative paths -- the writer, ONE resolver for the 7 readers, the 109 tracked JSONs scrubbed, a transcript-resolves test, no anonymize exemption (row R1, URGENT; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.1

## Why this exists
goal:g7.16.1.2 (bundle 2) row R1, first and URGENT: it blocks the Prime's PASS B3 (17:47Z 09-29). Measured 12:5xZ: 109 tracked `.agi/sessions/rotations/*.json` records carry the box user's home path. rotate.py writes the home-prefixed fields (handover.join.transcript · handover.join.path · transcript_path · after_join.results[].cmd/output · s12_self_reap ps_before), and the council measured 7 readers of join.transcript / transcript_path (rotate.py:2322 · 3011 · 3079 · 6581 · 6750 · 7018 · 7562), only 1 of which expands `~`.

## Target end-state
- rotate.py writes those fields in the `~`-relative form. Every reader goes through ONE resolver that expands `~` (config-max: the prefix form lives in one place).
- The 109 records are scrubbed to the same form in the same round. A committed test loads a scrubbed record and resolves its transcript to an existing file.
- anonymize.py gains NO exemption.

## Invariants
- A rotation record written before the round still resolves (the resolver accepts the absolute form too).
- No reader opens a `~`-prefixed path without expanding it.

## Falsifier
1. The resolver test passes, and `git diff d6cfe7749 HEAD > /tmp/b2.diff && python3 extensions/agi/bin/anonymize.py check --root .agi --diff-file /tmp/b2.diff` exits 0.
2. Negative: `git grep -lF "$HOME" -- '.agi/sessions/rotations/*.json' | wc -l` prints 0.

## Out of scope
goal:g7.16.1.2.3 (the generic home class over nodes) · the unified-diff readers (bundle 2 Out of scope)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Closed by the council, outcome:council-bundle-2 (self-perpetuating 23:5xZ 09-29; alive agreed). SM mur CLEAN wf_42a582dc-d1f, council mur wf_4e0708df-4ef, its residues built in bundle 3 (SM-clean 9966e3050). This row read in the bytes: test_rotation_record_home.py 14 passed 1 xfailed.
<!-- THOUGHT:END -->
