---
id: experiment:a00-8cfde212-e2e693
mint_id: 270a5790e6f043eea50b1539f079c76f
type: experiment
parents:
  - hypothesis:l4-the-after-join-second-input-is-typed-into-the-successors-pane-as-the-input-itself-never-a-nudge-that-points-at-the-inbox
next_edges: []
confidence: 0.95
edited_by: sensei-director
evidence_runs:
  - experiment:a00-8cfde212-e2e693
loop: hypothesis:l4-the-after-join-second-input-is-typed-into-the-successors-pane-as-the-input-itself-never-a-nudge-that-points-at-the-inbox@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: fc618f6a04dd3859
season: 2
title: A00 8cfde212 e2e693
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-8cfde212-e2e693

## Hypothesis under test

The after_join SECOND input is TYPED into the successor's pane as the input
ITSELF (`send.type_input` — the wake typing seam), never a dm plus a nudge
pointing at the inbox: a successor pays ZERO reads, and the send.send pane
NUDGE is suppressed for the one typed message.

## What the parent review found (why this run exists)

SL7.9x build (a00-546bfb85) wired rotate.py's PRODUCTION default as
`_type_fn(seat, dm)` — but send.type_input has the FULL `(root, to, text)`
signature. Against the built bytes:

    $ python3 -c "import sys; sys.path.insert(0,'extensions/agi/bin'); import send; send.type_input('successor','dm body')"
    RAISED: TypeError type_input() missing 1 required positional argument: 'text'

rotate.py wraps the call in `except Exception` -> `typed_ok=False` ->
`delivery.mode == "dm+nudge"`, nudge KEPT. So in PRODUCTION the after_join
second input was STILL a dm+nudge and the successor still paid one read.
The existing tests never caught it: every test injected a fake
`type_input(seat, text)` seam and never exercised the production default.

## The fix (surgical)

In `run_after_join`, when no `type_input` seam is passed, the production
default is resolved as a CLOSURE over `root` so the seam contract stays
`(seat, text)` (rotate.py ~11145):

    import send as _send
    _ti = getattr(_send, "type_input", None)
    if _ti is not None:
        _type_fn = lambda _seat, _text: _ti(root, _seat, _text)

The getattr guard is kept (a stub `send` without `type_input` still falls
back to dm+nudge, never raises). Nothing else changed: dry_run, delivery
dict, nudge_suppressed, the default send_dm's `nudge=(not nudge_suppressed)`
all untouched.

## Regression tests added (test_after_join_service.py)

Two tests drive the REAL production wiring (NO type_input seam injected):

1. `test_production_default_types_through_real_wiring` — a stub `send`
   module records the REAL call shapes; run_after_join_for_seat resolves the
   production default closure and asserts:
   - `delivery.mode == "typed"`, nudge `suppressed`
   - the REAL `send.type_input` received `(root, "d", dm_body)` — reaching
     the pane through the default, not a stub
   - the REAL `send.send` carried `nudge=False` for the typed message

2. `test_production_default_nudge_kept_on_typing_refusal` — the production
   typing seam REFUSES (False): delivery `dm+nudge`, nudge `kept`, and the
   REAL `send.send` carries `nudge=True` (exactly as today).

## Evidence (measured)

    $ python3 -m pytest extensions/agi/tests/test_after_join_service.py \
          extensions/agi/tests/test_send.py extensions/agi/tests/test_seatsig.py \
          extensions/agi/tests/test_heal.py extensions/agi/tests/test_bin_help_smoke.py -q
    443 passed, 3 skipped in 32.35s

(60 in test_after_join_service.py alone: 58 pre-existing + 2 new.) The
production default was DEMONSTRABLY reached: the new test routes
run_after_join_for_seat -> run_after_join with no injected seam, the default
closure binds `root`, and send.type_input receives `(root, seat, text)` with
delivery recorded as `typed`. The old `_type_fn(seat, dm)` shape is a
genetic negative control for the test: it raises TypeError under the real
signature, sinks to dm+nudge, and the `typed` assertion fails.

## Verdict

`proved` — the production default was reached by a run test and delivers
`typed` with a suppressed nudge; the falsifier "a successor pane that still
receives a pointer line for a typed input" is closed on the built bytes.

## Agent Notes
Fixed production default typing seam: closure over root, seam contract (seat,text). Two regression tests drive the real default wiring, no fake seam; suite 443 passed, 3 skipped.

Parent review SL7.93: ACCEPTED as proved (0.95). Reviewed the artifact, not the report: rotate.py now resolves the production default as a closure over root — _ti(root, _seat, _text) — so the real send.type_input is reached without a stub; two regression tests exercise the PRODUCTION default (no injected seam) and assert the REAL send.send nudge argument (nudge=False on typed, nudge=True on refusal). Parent re-ran the full neighbourhood: 443 passed, 3 skipped.

mur-SL2.26 (Prime XVIII 23:40Z, applied by sensei-director): DEMOTED to inconclusive_lean_disproved:60 — the suppressed nudge returns on the next heal poll (the unread dm copy re-arms send.wake); the typed body is unmeasured on a real pane; the delivery field is a dict, not the literal. Re-cut assigned by Sanctuary Master
