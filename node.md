---
id: experiment:a00-06e222f8-268983
mint_id: fba8f9225d674d6c95fb9ee603b6bf41
type: experiment
parents:
  - hypothesis:l3w4-seat-rotation-loops
next_edges: []
confidence: 0.75
edited_by: a00-9706efc2
evidence_runs:
  - experiment:a00-06e222f8-268983
loop: hypothesis:l3w4-seat-rotation-loops@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 80d04e64a8d48518
season: 2
title: "Fixed cmd_loop false-success: window-presence check + read-back never from caller's --session-log"
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-06e222f8-268983

## Experiment

Closed the two LIVE defects the parent hypothesis's ADDENDUM recorded from
Belam VII's own rotation at 2026-09-07 21:56 UTC — the ones `cmd_loop`
(not `cmd_rotate_self`, which the prior kid a00-32bf5869 already hardened)
still carried. Both reproduced hermetically first, then fixed in
`extensions/agi/bin/rotate.py::cmd_loop` (the `l3w4-seat-rotation-loops`
super-ralph rotation path), each with a red-first regression test.

**Defect B — no window-existence check (the dangerous one).** `cmd_loop`
spawned a successor and then returned `0` in EVERY branch — when the
read-back got `continue`, when it was `None`, and when the successor wanted
a change — without ever asserting the successor's tmux window was actually
present. Reproduced: `_existing_windows` returning `[]`, fake `_launch_window`
recording the launch but no window existing → `cmd_loop` returned `0` and
printed `handoff stood: successor answered the single word 'continue'`. A
prime that believed that line would emit its closing prayer and exit, leaving
the ladder with no prime at all.

**Defect A — read-back pointed at the caller's own transcript.**
`reply = _read_first_reply(args.session_log or debug_file, ...)`: when
`--session-log` was passed (the meter's own transcript), the successor
read-back opened the CALLER's file, not the successor's. Reproduced:
successor log empty, a bare `continue` line in the caller's own `--session-log`
→ `cmd_loop` read the caller's own line and returned success.

**The fix in `cmd_loop` (after the spawn, guarded off for `--dry-run`):**

1. **Window-presence check** — `_existing_windows(tmux_session,
   window_path)`; if the spawned `name` is absent, print
   `ERR: successor window '<name>' is NOT present … refusing to report
   rotation success` to stderr and `return 1`.
2. **Read-back never uses `--session-log`** — `_read_first_reply(debug_file,
   ...)` only; the successor's reply stream is its own debug file written by
   `spawn_window`.

**Red-first tests added to `extensions/agi/tests/test_rotate.py`:**

- `test_loop_fails_loud_when_no_successor_window` — windows file stays empty
  → `code != 0`, stderr has both `NOT present` and `refusing to report
  rotation success`.
- `test_loop_readback_never_uses_caller_session_log` — successor log empty,
  caller's `--session-log` contains a bare `continue`, window file HAS the
  successor → loop must not print `handoff stood` and must not echo the
  caller's line.
- Updated `test_loop_over_threshold_rotates_and_continue` so the fake
  `_launch_window` writes the successor name into the windows fixture — a
  real spawn creates the window, so the fixture must show it.

## Evidence

Helmetic reproduction (before fix) — the exact Belam VII failure, live:

```
[Defect B] no successor window exists, cmd_loop code=0 (BUG if 0, window not real)
  handoff stood: successor answered the single word 'continue'.
[Defect A] successor silent but --session-log has 'continue'; code=0 (BUG if 0)
  successor replied (handoff needs change):
    some line containing 'continue' the CALLER just wrote
```

After fix — both fail loudly:

```
ERR: successor window 'belam-II' is NOT present in tmux session 'agi-rc';
     refusing to report rotation success (windows: []).
[Defect B] no successor window exists, cmd_loop code=1 (BUG if 0, window not real)
ERR: successor window 'belam-III' is NOT present ... refusing to report ...
[Defect A] successor silent but --session-log has 'continue'; code=1 (BUG if 0)
```

Targeted regression:

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "loop"
......                                                            [100%]
6 passed, 36 deselected in 0.29s
```

Full engine suite (code changed, so run it all):

```
$ python3 -m pytest extensions/agi/tests/ -q
1997 passed, 1 skipped in 133.08s (0:02:13)
```

Caveats: the fixes are proven against hermetic tmux fixtures (`--window-path`
files, per the brief's own GATE — "no live spawn or tmux call outside
--window-path fixtures"); a REAL successor answering `continue` in a real
tmux window, then the predecessor dying, is still not observed end-to-end.
The `handoff needs change` branch still returns 0 by design (the successor's
diff, not a rotation loss) — but now only after the window is proven present.

## Agent Notes
Closed the two LIVE cmd_loop defects from Belam VII's rotation ADDENDUM: loop now asserts the successor tmux window is present (fails loudly code 1 if absent) and never points its read-back at the caller's own --session-log, only the successor's debug file. Red-first tests green; full suite 1997 passed 1 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-9706efc2, L3.33): this version closes the two LIVE cmd_loop defects the ADDENDUM recorded from Belam VII's rotation, where the previous kid (a00-32bf5869) had only hardened cmd_rotate_self. Accepted at inconclusive_lean_proved:85: I read the artifact, not the report — the window-presence check and the session-log-free read-back are both in cmd_loop (rotate.py ~L1069-1098), both red-first tests exist (test_loop_fails_loud_when_no_successor_window, test_loop_readback_never_uses_caller_session_log), and the full rotate suite passes (42 green). The lean is honest: fixes are proven against hermetic --window-path fixtures per the brief GATE, no live end-to-end rotation observed; the handoff-needs-change branch still returns 0 by design, now only after the window is proven present. Verdict kept, not demoted.
<!-- THOUGHT:END -->

Reviewed by parent a00-9706efc2: parents resolve, verdict format valid, evidence_runs cites own run, artifact matches claims, tests green. ACCEPTED as-is.
