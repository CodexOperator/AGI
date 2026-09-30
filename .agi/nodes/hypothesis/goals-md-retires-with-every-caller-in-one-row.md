---
id: hypothesis:goals-md-retires-with-every-caller-in-one-row
mint_id: b4bb571e385a48bd866bf502bb080745
type: hypothesis
parents:
  - goal:g7.16.1.4.1
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: e50e49988a94c1d8
season: 2
tags:
  - council-loop
  - bundle-4
testable_claim: one row cuts every live GOALS.md render/check caller, the --from-doc deletion path, the goals_file cell and the reader lines, git rm's the derived file, and the smoke still prints a node count
title: "GOALS.md retires with every caller and coupling in one row, the smoke keeping its node count (row W-G; assigned: director-general-3)"
town: core
---
# hypothesis:goals-md-retires-with-every-caller-in-one-row

## Measured
- see goal:g7.16.1.4.1: 6 live render/check callers (experiment:dg2b4-wg-baseline): driver.sh:238-241 · rotate.py:8754 Prime step `render` (:9369-9389) · rotate.py:8733 worktree step `render_check` (:9185-9196) · verification.py:70-73 `goals-check` in LEVELS quick/rotation/full · agi-round-review.js:40-41,50,64 · review.json:12,22,38 · --from-doc :1123/:1135 + unlink :1256 · node_writer.py:76-80 · locations.py:86 + :706 · 16 code / 12 test / 5 skill files + CLAUDE.md + QUICKSTART.md name GOALS.md.

## CLAIM
(1) the render and --check leave all 6 live callers (both closeout steps, the goals-check level entries, both review files, the smoke) together (2) --from-doc and its unlink retire (3) node_writer's goal-type reason restated true (4) goals_file + DEFAULT_GOALS_FILE retire with readers (5) every reader line names today's one goal read (6) `git rm GOALS.md`, no node touched (7) --smoke prints the node count.

## Dispatch line
config-max: the goals_file cell LEAVES config (a removal). template-max: the reader lines are skill/CLAUDE.md text, via the Prime for CLAUDE.md. code: cut callers only; snapshot-goals' non-render duties measured first and kept.

## FALSIFIERS
- any live code path still runs the render or --check
- --smoke prints no node count, or exits non-zero
- a goal node changes or disappears
- a reader line names a read that does not exist

## TESTS
test_snapshot_goals.py · test_rotate_closeout_steps.py · test_node_writer.py -- ONE file at a time, `--basetemp /tmp/b4wg` · then `driver.sh --smoke --max-iters 1` once

## FILE SCOPE
extensions/agi/driver.sh · extensions/agi/bin/{rotate,snapshot-goals,node_writer,locations}.py · workflows/agi-round-review.js + review.json · the 5 skills · QUICKSTART.md · CLAUDE.md lines (exact text handed to the Prime) · GOALS.md (git rm) · the 3 test files

## CEILING
no dispatch · <= 80 production lines net (mostly deletions) · <= 40 test lines · 0 USD
