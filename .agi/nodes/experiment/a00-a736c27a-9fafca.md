---
id: experiment:a00-a736c27a-9fafca
mint_id: 8ef8daa89fe342328a449c7af54d31de
type: experiment
parents:
  - hypothesis:cold-seat-brief-five-pane-routes
next_edges: []
confidence: 0.78
edited_by: a00-a736c27a
evidence_runs:
  - experiment:a00-a736c27a-9fafca
line_ceiling: 40
loop: hypothesis:cold-seat-brief-five-pane-routes@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 7811cdaddaa5fae6
season: 2
title: Five pane-facing routes + engine seams listed in the cold-seat PROFILE with a red-on-absence proof
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a736c27a-9fafca

## Experiment

**Claim judged:** `hypothesis:cold-seat-brief-five-pane-routes` — falsifier 1 of
`goal:g7.31.3.1`.

**Surface chosen (ONE):** `doc:director-grok-internals` `SECTION:PROFILE`
(candidate 1). Why: it is the region the sync recipe names as the source of a
cold grok seat's profile description — `doc:grok-harness-internals-sync`
`SECTION:ROUTINE_SYNC`: `SECTION:PROFILE → from per-post SoT → profile
description`. Candidate 2, `extensions/agi/briefs/director-belam-duties.md:14`,
carries the five route names but is not the surface the grok sync pulls; left
untouched and named as a residual in the report's caveats.

**Pre-fix measurement** (`write.py doc:director-grok-internals 'read body 131:131'`):

```
routes: write.py · read · send · dispatch/workflow · rotate/spawn
```

Red on two counts: the route `write` is named only by its seam `write.py`, and
five of six seam tokens (`commands.py`, `viewport`, `send.py`, `dispatch.py`,
`workflow.py`, `rotate.py`) are absent. The checker returned 14 violations on
these live bytes (first: `missing route 'write'`).

**Build (the claim is behaviour, not a measurement):** one body line replaced
(`write.py doc:director-grok-internals 'replace body 131:131 -'`) with:

```
routes: write (write.py) · read (commands.py+viewport) · send (send.py) · dispatch/workflow (dispatch.py+workflow.py) · rotate/spawn (rotate.py)
```

**Proof:** added `extensions/agi/tests/test_cold_seat_five_routes.py`. It
extracts the `routes:` line out of `SECTION:PROFILE` of the LIVE node, requires
the five contract names plus the seam tokens, and runs the same checker over
mutated copies of the live bytes: drop a route → red, add a sixth route → red,
drop a seam → red. A wire test asserts `SECTION:PROFILE` and `per-post SoT`
appear in `doc:grok-harness-internals-sync` `SECTION:ROUTINE_SYNC`.

## Evidence

Pre-fix (`python3 -m pytest extensions/agi/tests/test_cold_seat_five_routes.py -q`):
`1 failed, 4 passed` — `test_real_brief_names_all_five_routes_and_seams`
failed on the live brief. Post-fix: `5 passed in 4.37s`. The three mutation
tests pass against the live bytes, so the checker is demonstrably non-vacuous.

Measured production lines: 2 (the doc-node body line; the test file is
excluded). Ceiling 40 — no re-brief needed.

## Agent Notes
Built the cold-seat PROFILE routes line to name all five contract routes and their engine seams; added a live-bytes checker test that goes red on a deleted route, a deleted seam, or a sixth route; pre-fix red / post-fix 5 passed.
