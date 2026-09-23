---
id: experiment:a00-f7cab927-b7dd7e
mint_id: a6a69c3232314a6fba189ab2e9f46fad
type: experiment
parents:
  - hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session
next_edges: []
confidence: 0.75
edited_by: a00-f7cab927
evidence_runs:
  - experiment:a00-f7cab927-b7dd7e
line_ceiling: 40
loop: hypothesis:alarms-loop-runs-flat-and-the-capture-grace-restarts-per-session@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 79
profile: balanced
role: kid
scaffold_hash: 798e8886ad59c4ef
season: 2
title: Alarms loop flattened, capture stamp scoped per session, captive ratio off by name
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f7cab927-b7dd7e

## Experiment

Build round, not a measurement: all three EF.22 conjuncts implemented in the
engine bytes, one new test each, every test proved RED on pre-fix bytes first.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Why this version: conjunct 2 needed a decision. I took option (a) — name the
WRITING session on the stamp and have the reader treat a stamp whose session
differs from the seat's current one as ABSENT — over option (b) clearing the
stamp on rotate, because (b) has no single choke point while (a) is one read
plus one write. "Current session" is the hook payload's `session_id`, falling
back to the seat row's `session_id`/`session_ref` only through the existing
`_seat_latch_identity` path; the force-capture read gets the payload id
passed in. When the current session CANNOT be known (empty id) or the stamp
predates the field (no `session`), the stamp stands — same per-boot grace as
before, deliberately conservative: a wrong "absent" would force-capture every
prompt of an unknown session and never let its grace elapse. The write only
re-stamps when the existing stamp explicitly names a DIFFERENT session, so a
legacy/no-session stamp is not reset every prompt.
<!-- THOUGHT:END -->

### (1) `rotate.py` cmd_alarms — flat loop (line 7237-7298)
The `--once=False` tail was `while True: time.sleep(...); return cmd_alarms(args, root)`
— one stack frame per interval. Now the whole metering pass is the body of a
single `while True:` and the tail is `if args.once: return 0` then
`time.sleep(args.interval)`; the per-pass body is byte-for-byte the former
body, only its indentation moved. `--once` still returns 0 after one pass.

RED (pre-fix): `test_alarms_loop_is_flat_no_frame_growth`
(test_rotate_alarms_captive.py) drives 800 passes with `rotate.time.sleep`
monkeypatched and `_load_seats` spying the frame depth each pass. Pre-fix:
`AssertionError: (36, 835)` — depth grew a frame per pass. A 1500-pass variant
crashed with RecursionError near depth 990. After: max == min (constant).

### (2) `rotation_alert.py` force-capture stamp — scoped to the writing session
- write (main, ~1420-1446): the stamp now carries `{"first": t, "session": sid}`;
  it is re-stamped when an existing stamp explicitly names a DIFFERENT session
  (so the successor's own grace clock starts). A legacy stamp with no `session`
  is left alone.
- read (`_maybe_force_capture` line 788): a stamp naming a session other than
  the current `session_id` reads as ABSENT (`return False, None`). Unknown
  current session or a legacy stamp -> the stamp STANDS (never a silent reset).
- both call sites pass the session id (`_gated_rotate` line ~1066 already had
  it; main passes `session_id or ""`).

RED (pre-fix): `test_successor_session_waits_the_full_capture_grace`
(test_rotation_alert_capture.py) plants a 10-min-old stamp NAMED `s-A`, then
runs session `s-B`; pre-fix `_CAPTURE_LOGGED` held the 2 capture argvs at once.
Complement `test_same_session_old_stamp_still_captures` proves a
current-session old stamp still captures.

### (3) `rotation_alert.py` `_captive_rotate` — no 0.85 literal (line 875-895)
Guard is now `"captive_rotate_ratio" not in ladder -> False`; an unparseable
ratio returns False instead of falling back to 0.85. The idle-lane read in
`rotate.py` (which already used None) is untouched.

RED (pre-fix): `test_masters_only_without_ratio_is_off_by_name` and
`test_unparseable_ratio_is_off_by_name` (test_rotation_alert_captive.py) — both
failed pre-fix (capture fired at f=0.42 >= 0.85*0.4).

## Evidence

Red-first, on the pre-fix bytes before any edit:
- `python3 -m pytest extensions/agi/tests/test_rotate_alarms_captive.py -k flat_no_frame_growth -q`
  -> FAILED, `AssertionError: (36, 835)` (log red_conj1b.txt)
- `python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py -k successor_session_waits -q`
  -> FAILED, `_CAPTURE_LOGGED` held 2 capture argvs
- `python3 -m pytest extensions/agi/tests/test_rotation_alert_captive.py -k "masters_only_without_ratio or unparseable_ratio" -q`
  -> 2 failed

Green after the build:
- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_alarms_captive.py extensions/agi/tests/test_rotate_alarms_idle.py -q`
  -> `343 passed`
- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py extensions/agi/tests/test_rotation_alert_capture.py extensions/agi/tests/test_rotation_alert_captive.py -q`
  -> `77 passed`

Production lines: `git diff --numstat` over the two production files = 79
added / 55 deleted / net 24 (most of the delete/add is the pass-body
reindentation in conjunct 1). Net is under the 40-line ceiling; added lines are
under the 2x (80) stop line, so no re-brief was filed.

## Caveats
- The recursion defect is fixed but no run of the real alarms loop was made
  (per the brief, sleep is monkeypatched in every test).
- A stamp written by a session whose id is unknown falls back to the pre-fix
  per-boot grace; deliberate, but the fix is only as good as the payload's
  `session_id`.

## Struggles
- The kid-tier conftest gate refuses `file.py::test_name` node ids because
  `_named_paths` only treats args ending in `.py` as targeted; I used `-k`.
- The suite lock (`verify-suite.lock`) was held by a live parallel runner and
  refused two early runs; retried.
- `time.sleep` monkeypatched globally was called ~8.8x per pass under pytest
  (some pytest/libc path), so the first test's stop condition keyed on sleep
  count fired early; re-keyed on the load count.

## Agent Notes
All three EF.22 conjuncts built and red-first proved: cmd_alarms flattened to a while-loop (depth constant over 800 passes vs 36->835 pre-fix), force-capture stamp scoped to the writing session (successor waits its own grace; legacy/unknown session stands), and _captive_rotate's 0.85 literal removed (absent/unparseable ratio off by name). 343 + 77 tests green.
