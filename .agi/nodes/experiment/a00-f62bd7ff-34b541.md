---
id: experiment:a00-f62bd7ff-34b541
mint_id: cecf0438154f4582a93464c665d68d0c
type: experiment
parents:
  - hypothesis:l4-a-seat-is-a-post-everywhere
next_edges: []
confidence: 0.9
edited_by: a00-930daa46
evidence_runs:
  - experiment:a00-f62bd7ff-34b541
loop: hypothesis:l4-a-seat-is-a-post-everywhere@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 7259b46d41195128
season: 2
title: A00 f62bd7ff 34b541
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f62bd7ff-34b541

## Experiment

L4.306 FIX-ONLY (kid 1 of 4 under hypothesis:l4-a-seat-is-a-post-everywhere).
Measured the THREE sites that still bypassed the geometry resolver and would
break once the Prime runs `cli.py post-rename --apply` on the live tree, then
routed each through `geometry_config.resolve` (post-first, one-season seats
alias):

1. `extensions/agi/bin/send.py` `_row_write_submit` (~L336): hardcoded
   `Edit("config:seats")` + `verb_set(e, "seats", ...)`. Now resolves
   `_, list_key = geometry_config.resolve(graph)`, writes `Edit(f"config:{list_key}")`
   and `verb_set(e, list_key, ...)` — matching rotate._write_identity_cells.
   Note-on-failure path and behaviour unchanged; docstring corrected to
   post-first with seats as the one-season alias.

2. `extensions/agi/bin/sensei.py` `load_seats` (~L58): hardcoded
   `node_writer.find_node_file(root, "config:seats")` which returns None once
   the node file is posts.md, so all ~7 callers would get `[]`. Now resolves
   `path, list_key = geometry_config.resolve(root)`, reads that file, and
   parses the `{list_key}:` block; added `geometry_config` to both the package
   and plain-script import blocks.

3. `extensions/agi/bin/viewport.py` `_anchor_index` (~L901): read
   `(gf.get("config:seats") or {}).get("seats") or []`. Now reads
   `config:posts`/`posts` first, falling back to `config:seats`/`seats` (the
   same posts-first local fallback the sibling reader at L497 uses).

Tests added to `extensions/agi/tests/test_geometry_config.py`: posts.md-only
fixture for each site (residual seats literal would read empty/absent and
FAIL) plus a seats.md-only fixture proving the alias fallback still works —
6 new tests, send's writer site asserted via a fake `write.submit` capture.

## Evidence

`env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_geometry_config.py extensions/agi/tests/test_send.py extensions/agi/tests/test_seat_status.py extensions/agi/tests/test_viewport.py -q`
last line: **304 passed in 5.21s**

Focused new tests: `-k "row_write_submit or load_seats or anchor_index"`
→ **6 passed, 11 deselected in 0.83s**

The sensei resolver change exposed a stale `seat_fixture` in test_sensei.py
that wrote the row to `nodes/config/seats.md`; the live/canonical seat
registry is `nodes/.geometry/seats.md` (geometry_config.resolve only reads
.f. geometry, never a node-id scan — the live tree has no `nodes/config/`).
Fixture moved to nodes/.geometry/seats.md; full sensei + hierarchy set then
passes (128 passed), and the whole target set passes:
`... test_geometry_config.py test_send.py test_seat_status.py test_viewport.py test_sensei.py -q`
→ **311 passed in 4.46s**

Did not touch: rotate.py, cli.py, hooks/, adapters/, graphweb.py,
spawn_budget.py, prose files, the live `.agi/nodes/.geometry/seats.md`, the
schema. No `post-rename --apply` on the live tree.

## Agent Notes
Routed send._row_write_submit, sensei.load_seats, viewport._anchor_index through geometry_config.resolve post-first (seats alias fallback). 6 new tests (posts-only + seats-only fixtures) in test_geometry_config.py; fixed stale test_sensei seat_fixture (nodes/config->.geometry). 311 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review L4.306 (a00-930daa46): reviewed the ARTIFACT, not the report. Verified in the bytes: send._row_write_submit now resolves `_, list_key = geometry_config.resolve(graph)`, writes Edit(f"config:{list_key}") and verb_set(e, list_key, ...) with the note-on-failure path unchanged; sensei.load_seats resolves (path, list_key) through geometry_config, guards a None/missing path, and parses the {list_key}: block; viewport._anchor_index reads config:posts/posts first then config:seats/seats. Ran the four named files myself: 304 passed in 4.15s, plus test_sensei.py 7 passed. ACCEPTED proved for this slice.
<!-- THOUGHT:END -->

L4.306 kid1 ACCEPTED proved (parent a00-930daa46): send._row_write_submit + sensei.load_seats + viewport._anchor_index routed through geometry_config.resolve post-first/seats-alias; 304 passed on the four named files, test_sensei 7 passed.
