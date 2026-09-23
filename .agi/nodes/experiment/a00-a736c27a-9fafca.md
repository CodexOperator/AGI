---
id: experiment:a00-a736c27a-9fafca
mint_id: 8ef8daa89fe342328a449c7af54d31de
type: experiment
parents:
  - hypothesis:cold-seat-brief-five-pane-routes
next_edges: []
confidence: 0.78
edited_by: a00-4d46690b
evidence_runs:
  - experiment:a00-a736c27a-9fafca
line_ceiling: 40
loop: hypothesis:cold-seat-brief-five-pane-routes@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "check(live bytes) with rotate/spawn deleted from the routes line", "expected": "non-empty violations naming 'missing route rotate/spawn' and 'missing engine seam rotate.py'", "observed": "['missing route \\'rotate/spawn\\'', \"missing engine seam \\'rotate.py\\'\"]", "result": "held"}
  - {"conjunct": 2, "class": "gate", "cmd": "check(live bytes) with ' · grok-only (sneaky.py)' appended", "expected": "non-empty violations naming unexpected route 'grok-only'", "observed": "[\"unexpected routes [\\'grok-only\\']\"]", "result": "held"}
  - {"conjunct": 3, "class": "wire", "cmd": "grep -n '^routes:' doc:director-grok-internals + SECTION headings; WIRE doc strings", "expected": "routes line inside SECTION:PROFILE (line 55..192), sync doc names SECTION:PROFILE + per-post SoT", "observed": "routes at 152; PROFILE 55; ROUTINE_SYNC 193; WATCH 205; in-PROFILE=True; sync names both=True", "result": "held"}
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW DH.183, agent a00-4d46690b over kid a00-a736c27a.

(1) WHAT THE INSTRUCTION SAID. `goal:g7.31.3.1` falsifier 1: "A cold seat brief / custom-instruction surface lists the five routes by the names in the `goal:g7.31.3` table (or records a deliberate rename with old→new). Grep/read proof on the brief artifact." My hypothesis added: each mapped to its engine seam, and the proof goes red on absence or a sixth route.

(2) WHAT THE MACHINE ACTUALLY DOES, read in the moved bytes and RUN. The kid's diff is exactly two paths: `.agi/nodes/doc/director-grok-internals.md` line 152 and the new `extensions/agi/tests/test_cold_seat_five_routes.py`. Line 152 now reads `routes: write (write.py) · read (commands.py+viewport) · send (send.py) · dispatch/workflow (dispatch.py+workflow.py) · rotate/spawn (rotate.py)` — five segments, five contract names, six seam tokens. The test extracts the `routes:` line out of the `### SECTION:PROFILE` block (heading at line 55) of the LIVE node bytes and runs the same extractor over mutated copies. My own probes, run against the live artifact: real bytes -> `[]`; delete rotate/spawn -> `["missing route 'rotate/spawn'", "missing engine seam 'rotate.py'"]`; append `grok-only (sneaky.py)` -> `["unexpected routes ['grok-only']"]`; delete the line -> `["SECTION:PROFILE has no routes: line"]`; the routes line sits at 152, inside PROFILE (55) and before ROUTINE_SYNC (193); `doc:grok-harness-internals-sync` names both `SECTION:PROFILE` and `per-post SoT`, and its SECTION:ROUTINE_SYNC maps `SECTION:PROFILE → from per-post SoT → profile description`. `pytest test_cold_seat_five_routes.py -q` -> 5 passed. No sixth grok route in `dispatch.py`/`rotate.py` (`grep -Ein 'grok.?(only|route)'` empty).

(3) THE NEAR MISS. A checker that only asserts the five names exist in the file would pass on the OLD line too (`write.py · read · send · dispatch/workflow · rotate/spawn` names the seams only by accident — 5 of 6 seam tokens absent), and would keep passing after the line drifted into `SECTION:ROUTINE_WATCH`. Two things prevent that: the extractor scopes to `SECTION:PROFILE`, and the mutation tests make the checker non-vacuous. A second near miss: naming `write` only as `write.py` satisfies "mentions write" while losing the contract name; the checker requires the bare token.

(4) DEVIATION. None from the parent's standing rules. No git was run: the kid shares this worktree, so its moved bytes were read directly at `doc/director-grok-internals.md:152` and in the new test file, not via `git diff`.

VERDICT: proved. The artifact is a cold-seat surface (profile SoT the grok sync applies), carries all five contract names and all six seams, and the red-on-absence proof is non-vacuous. Residual named, not ridden: `extensions/agi/briefs/director-belam-duties.md:14` also carries a five-name route line but is not the grok sync surface; left untouched.
<!-- THOUGHT:END -->
