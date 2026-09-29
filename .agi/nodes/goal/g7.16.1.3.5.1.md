---
id: goal:g7.16.1.3.5.1
mint_id: d4c8198f093f41c98eed29c91c99422e
type: goal
parents:
  - goal:g7.16.1.3.5
next_edges: []
confidence: 0.6
edited_by: director-general-1
goal_id: G7.16.1.3.5.1
goal_kind: subgoal
heading_level: 6
origin: goals-doc
scaffold_hash: 6618fafa79447e0c
season: 2
seeds: []
status: retired
tags:
  - formation
  - council-loop
  - bundle-3
  - local-maxxing
  - row-g
title: "G7.16.1.3.5.1: the render and its gates retire -- driver smoke, verification goals check and snapshot-goals --render/--check gone, the helper library kept, GOALS.md removed (row G part 1; assigned: director-general-1)"
town: core
---
# goal:g7.16.1.3.5.1

## OWNER 2026-09-29 17:3xZ (via belam, relayed by the convener at 2eb4f4528), verbatim
"Go ahead and retire GOALS.md. We don't need it anymore stop bothering with it or the render byte round trip script"

## Why this exists
goal:g7.16.1.3.5 (row G), part 1: the machinery. The render and its round-trip gate run in `driver.sh --smoke` (its render step), verification.py's goals check and `snapshot-goals.py --render/--check`. snapshot-goals.py's helpers are imported by 10 bin modules, so the FILE cannot retire, only its render duty can.

## Target end-state
- driver.sh --smoke has no render step. verification.py has no goals round-trip check. `snapshot-goals.py --render/--check` are removed, or refuse with a one-line retirement pointer.
- The library functions stay importable, with every importer unchanged. A duty other than rendering that the render path carried (e.g. warn_premature_complete, report_integrity) is kept on a live path, or its retirement is named.
- GOALS.md is removed from the tree in this row.
- CUT THE CALLERS, every coupling named on goal:g7.16.1.3 row G (30f4db55f, e662637ac), in this SAME row: (1) the rotation closeout step render (rotate.py closeout step + handler) and its row in test_rotate_closeout_steps.py, since a failed render refuses EVERY rotation · (2) driver.sh --smoke render · (3) workflows/agi-round-review.js + workflows/review.json render --check gate · (4) CRITICAL: snapshot-goals.py --from-doc AND its unlink retire, the ONLY code that turns GOALS.md into goal-node DELETIONS (a stale GOALS.md restored from git + one --from-doc run prunes live goals) · (5) the closeout --check gate, which compares against an empty string once the file is gone and refuses forever · (6) node_writer's stated reason for keeping goal out of CANONICAL_NODE_TYPES is restated or goal is admitted · (7) the goals_file config cell + locations.py DEFAULT_GOALS_FILE (with its test) retire, and the verify_unified / links / unify / dashboard readers are cut.

## Invariants
- Node count unchanged. `links.py links` = 0 broken (a link to GOALS.md is repointed, not left dangling).

## Falsifier
1. `bash extensions/agi/driver.sh --smoke --max-iters 1` exits 0, and `python3 extensions/agi/bin/commands.py run verify` passes with no goals-render check.
2. Negative: `git grep -n 'snapshot-goals.py --render' -- extensions ':!extensions/agi/tests'` prints 0, one rotate closeout runs clean, `git grep -n 'from-doc' -- extensions/agi/bin/snapshot-goals.py` prints 0, and `git grep -nE 'render.*--check|--render' -- extensions/agi/driver.sh extensions/agi/bin/verification.py` prints 0.

## Out of scope
goal:g7.16.1.3.5.2 (doc citations)

## Agent Notes
Assigned to **director-general-1**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Retired by director-general-1 (20:4xZ 09-29): the council moved row G UNBUILT from bundle 3 to bundle 4 (20:2xZ), where it is ONE row, goal:g7.16.1.4.1 (row W-G). Superseded, not failed: the couplings measured here travel into that leaf.
<!-- THOUGHT:END -->
