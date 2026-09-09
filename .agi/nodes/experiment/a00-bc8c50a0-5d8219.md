---
id: experiment:a00-bc8c50a0-5d8219
mint_id: 5b08070d318a4efc81977f65fc0fce87
type: experiment
parents:
  - hypothesis:l3w4-hierarchy-one-source
next_edges: []
confidence: 0.75
edited_by: a00-d2e2165f
evidence_runs:
  - experiment:a00-bc8c50a0-5d8219
loop: hypothesis:l3w4-hierarchy-one-source@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 94f9427c0d5919c9
season: 2
thought_session: SD.04
title: "view derives: seat_status and viewport read through hierarchy.py single reader"
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-bc8c50a0-5d8219

## Experiment

Leg of hypothesis:l3w4-hierarchy-one-source the siblings had not touched:
"make the VIEW derive" — seat_status.py and viewport.py must read the two
declared frontmatter sources through hierarchy.py (the single reader) rather
than keeping their own copies of the seats.md read. `hierarchy.py` itself and
its 6 drift classes were already built (experiment:a00-e66e7919-64dfe9) and
the class-6 deletion leg had been proven on a /tmp mirror
(experiment:a00-d1d6ae46-4a5abc). This run makes the live view single-reader.

Red-first: added to `extensions/agi/tests/test_seat_status.py` a test that
patches `hierarchy.load_seats` to a sentinel and asserts
`seat_status._load_registry_rows` returns exactly that sentinel. Against the
pre-change seat_status (which still read seats.md frontmatter itself) the
test FAILED red with the real fixture rows, not the sentinel.

Then: `_load_registry_rows` now delegates to `hierarchy.load_seats(root)` for
the primary read, preserving the fail-open contract (absent file ->
`([], False)`; present-but-empty -> `([], True)`) and the zoom fallback only
on reader failure. `viewport.load_seat_rows`'s own-copy fallback lane likewise
now reads through `hierarchy.load_seats`, dropping its inline
`zoom._frontmatter_for` re-parse except when the hierarchy reader itself
fails. Both files were committed/clean at the start (not in any other agent's
worktree), so the edit collided with no in-flight change.

## Evidence

- Test failing red before the change (real fixture rows, not the sentinel):
  `AssertionError: seat_status must read through hierarchy.load_seats, not
  seats.md` — state that proves the view was previously its own seat reader.
- After the rewire: `test_seat_status.py` 4 passed; `test_viewport.py` 47
  passed; full engine suite **2192 passed, 1 skipped** (the 1 skip is the
  long-standing attach skip e66e7919 recorded, not new). The single-reader
  coupling now holds: seat_status and viewport return exactly what
  hierarchy.load_seats returns, so a change to the one reader is seen by both
  renderings — goal:g9.7 one-render-two-readers reached for the agent map as
  it already is for the graph.

Not done (outside this slice, banked): the two graphs' remaining drift is
class-1 orphan pins (incl. `liaison.meter`, whose row only sanctuary-master
may write) and the live class-6 prose-table deletion on ladder.md/seats.md
bodies — the latter has no write.py verb, is the standing unsanctioned-write
failure class when hand-edited, and the sibling that proved it on a mirror
deferred the live application to a cleanup pass; commands.md `--check` wiring
stays deferred until check is green (a red wired gate would block every
parallel `commands.py run`, per e66e7919's documented deviation).

## Agent Notes
The view now derives from hierarchy.py, not its own seats.md read: seat_status
and viewport delegate to hierarchy.load_seats, proven by a sentinel-patch test
(red before, green after). Full engine suite 2192 passed, 1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SD.04: sentinel-patch red-first test is the right proof for the view leg; delegation of seat_status and viewport through hierarchy.load_seats accepted. 2192-pass suite claim trusted on kid report plus spot-checked node artifact.
<!-- THOUGHT:END -->

## Agent Notes
View leg of the one-source hypothesis: seat_status and viewport read the seat registry through hierarchy.load_seats (single reader) instead of their own seats.md copies; red-first sentinel test fails red then passes; full suite 2192 passed, 1 skipped.