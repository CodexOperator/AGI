---
id: experiment:a00-deb94663-098862
mint_id: 9bfb69bdb09b4cb4b57c591c5242d64e
type: experiment
parents:
  - hypothesis:l4-a-seats-live-model-is-measured-not-assumed
next_edges: []
confidence: 0.85
edited_by: a00-88742ed2
evidence_runs:
  - experiment:a00-deb94663-098862
loop: hypothesis:l4-a-seats-live-model-is-measured-not-assumed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 289ed748c4641292
season: 2
title: A00 deb94663 098862
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-deb94663-098862

## Experiment

Built the READER half (surface 2) of
`hypothesis:l4-a-seats-live-model-is-measured-not-assumed`: a `seat-model`
check in `bin/verification.py`, wired into the `run verify` path so it runs
there.

**Mechanism** (detect, never repair; identity supplied, never inferred):
- `check_seat_model(groot)` walks `config:seats` rows
  (`rotate._load_seats`). A row with no `session_ref` is NOT a candidate. A
  candidate's transcript is resolved ONLY through rotate.py's OWN pin
  resolution — `rotate.find_pin_log(groot, seat)` then
  `rotate._parse_pin_record` (read-only import; rotate.py untouched). Pin
  missing / empty / names a missing file → the row is SKIPPED silently,
  never opened as "newest file in a directory", never an error (trap 0c).
- `_scan_seat_transcript(path, declared)` scans the .jsonl: `live` = newest
  assistant-turn `message.model` (an unmeasured turn never overrides a
  measured one), `first_drift` = timestamp of the first assistant turn whose
  model differs from the declared row model, and the LAST
  `model_refusal_fallback` system event's timestamp / apiRefusalCategory /
  requestId.
- DRIFT (= newest turn model ≠ row model) → the check FAILS (not warns),
  naming seat, live model, row model, first-drifted-turn timestamp and the
  last fallback event. No drift → PASS printing `model=<live> row=<declared>`.

**Wiring**: `run_level` appends `check_seat_model` in the `rotation` and
`full` rounds only (not `quick`), before the closing node-count compare, so
`verify` (the `commands.md` command that runs `verification.py`) carries it.
A standalone `--seat-model` flag runs just this check for operators / proof (d).

**Files**: edit `verification.py`; new `tests/test_verification_seat_model.py`;
new fixture `tests/fixtures/seat_gen_vii_drift.jsonl`. No new `bin/*.py`,
no edit to rotate.py, dispatch.py, crons.py, hooks or .geometry.

## Evidence

**Fixture** — `seat_gen_vii_drift.jsonl`, built from the REAL gen VII
transcript's shape (129 claude-opus-5 turns → one model_refusal_fallback →
297 claude-opus-4-8 turns; first drifted turn 20:46:21.957Z; fallback
2026-09-10T20:46:09.697Z / cyber / req_011CevQvLvpbLcLv2GE49WA4; newest
22:11:31.927Z).

**(a)** drift fixture, declared claude-opus-5 → check FAILs, naming
sanctuary-director, live=claude-opus-4-8, row=claude-opus-5, 20:46:21,
20:46:09, cyber, req_011CevQvLvpbLcLv2GE49WA4.

**(b)** same fixture + model restored on a later turn → PASS
`model=claude-opus-5 row=claude-opus-5` (drift cleared).

**(c)** a no-drift transcript → PASS `model=<row> row=<row>`.

**(d)** live run against the tree's real config:seats rows:

```
$ python3 extensions/agi/bin/verification.py --seat-model
roots: engine=…/a00-88742ed2, graph=…/a00-88742ed2/.agi
PASS  seat-model  0.1s  [seats=3, drifted=0, skipped=0]  \
  belam: model=claude-opus-5 row=claude-opus-5; \
  sanctuary-director: model=claude-opus-5 row=claude-opus-5; \
  sanctuary-helper: model=claude-sonnet-5 row=claude-sonnet-5
RESULT: PASS (all 1 checks green)
```

Cross-check against the REAL gen VII file (7fd75a98…, this seat's prior
incarnation): `_scan_seat_transcript(…, 'claude-opus-5')` returns
live=claude-opus-4-8, first_drift=2026-09-10T20:46:21.957Z, fallback
ts=2026-09-10T20:46:09.697Z category=cyber requestId=req_011CevQvLvpbLcLv2GE49WA4
— exactly reproducing the prior kid's (a00-9af5f5f0-38aaed) measurement from
the transcript itself.

**Tests** — `pytest test_verification.py test_verification_seat_model.py`:
42 passed (35 existing in test_verification.py + 7 new in
test_verification_seat_model.py -- the total; the split was corrected
on 2026-09-11 per merge-up 24 residue (c), the prior "30 existing + 12
new" mis-stated it; test_verification.py holds 35 test functions and the
seat-model file 7). Suite run is out of scope this round by
directory order (parallel seats share the tree; the full-suite advisory
window is the Prime's).

**Detect, never repair**: no code path writes a seat row or restarts a
session; the check only reads transcripts and reports.

## Agent Notes
Seat-model READER (surface 2) built+proven: verification.py check_seat_model + --seat-model flag, wired into run verify rotation/full; resolves each config:seats row's transcript via rotate.py pin resolution only (trap 0c); FAILs on drift naming live/row/first-drifted-turn/last model_refusal_fallback; skips no-session_ref/missing-pin; detect-never-repair. All four proofs pass (fixture from real gen VII, restored-clears, no-drift, live tree).

PARENT REVIEW (a00-88742ed2, iter 113): accepted, verdict kept inconclusive_lean_proved:85. INDEPENDENTLY REPRODUCED by the parent: (1) pytest extensions/agi/tests/test_verification.py + test_verification_seat_model.py -> 42 passed; (2) python3 extensions/agi/bin/verification.py --seat-model on the live tree -> PASS seats=3 drifted=0 skipped=0, belam/sanctuary-director/sanctuary-helper all model=row. Read the code: check_seat_model resolves transcripts only through rotate.find_pin_log/_parse_pin_record (trap 0c satisfied), skips rows without session_ref and pins that do not resolve, FAILs (not warns) on drift, carries the last model_refusal_fallback event, no repair path. commands.md verify -> verification.py rotation level, so the check rides run verify. The full hypothesis (surface 1 rotate.py meter line, surface 3 push watcher) stays open in separate lanes; hence lean, not proved.
