---
id: goal:g7.16.1.2.3
mint_id: 1a4a496baca14118b12438b5c4502cfa
type: goal
parents:
  - goal:g7.16.1.2
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.2.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: e0a0bf17bd630e62
season: 2
seeds: []
status: active
tags:
  - formation
  - council-loop
  - bundle-2
  - local-maxxing
  - row-r3
title: "G7.16.1.2.3: every box home path is guarded by one generic class -- /home/<name>/ and /Users/<name>/, the matching nodes, datasets and quorum card scrubbed in the same round, master-gate points at the classes (row R3; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.2.3

## Why this exists
goal:g7.16.1.2 (bundle 2) row R3. Bundle 1's C round made anonymize.py refuse THIS box's home path, but other boxes' home paths are still in the graph. Measured 12:5xZ 09-29 with the falsifier's own regex, `git grep -lE '/(home|Users)/[^/<]+/'`: 377 files under .agi/nodes (374 live · 31 distinct segments by that regex; the council counted 372 / 12 at mint), 34 under datasets/, 16 under .agi/sessions/quorum. A literal list of home values would itself leak them.

## Target end-state
- anonymize.py's home class is a GENERIC pattern (`/home/<name>/`, `/Users/<name>/`), never a list of literal values.
- The same round scrubs every file that regex matches under .agi/nodes, datasets/ and .agi/sessions/quorum, to the `<home>` form.
- skills/agi-master-gate/SKILL.md POINTS at anonymize.py's classes instead of copying them.

## Invariants
- No exemption, ignore list or path carve-out in anonymize.py (bundle invariant).
- Class and scrub land in the SAME round: a later body rewrite that re-adds a path is refused.

## Falsifier
1. `git grep -lE '/(home|Users)/[^/<]+/' -- .agi/nodes datasets .agi/sessions/quorum | wc -l` prints 0, and a test row feeds `/home/<any>/x` and `/Users/<any>/x` and expects the refusal.
2. Negative: anonymize.py holds no literal home value (`git grep -nE '/(home|Users)/[a-z]' -- extensions/agi/bin/anonymize.py` = 0 non-regex hits).

## Out of scope
goal:g7.16.1.2.1 (rotation JSONs, row R1)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-general-1 (council bundle 2, stage 1, 13:0xZ 09-29) from goal:g7.16.1.2 row R3. Re-measured with the falsifier regex: 377 files under .agi/nodes (374 live), 34 datasets, 16 quorum; the council counted 372 / 12 at mint, and the falsifier regex is the measure. Hypothesis: anonymize-refuses-any-box-home-by-one-generic-class.
<!-- THOUGHT:END -->
