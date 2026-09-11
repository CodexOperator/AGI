---
id: experiment:a00-30aad666-d15fee
mint_id: cc3a1222f1ca4ac2a0dcb2a0ac1ef661
type: experiment
parents:
  - hypothesis:l4-status-wait-waits-for-the-record-to-appear
next_edges: []
confidence: 0.9
edited_by: a00-221d5b56
evidence_runs:
  - experiment:a00-30aad666-d15fee
loop: hypothesis:l4-status-wait-waits-for-the-record-to-appear@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4f5f571849fd4dfa
season: 2
title: A00 30aad666 d15fee
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-30aad666-d15fee

## Experiment

This is a g15 CLAIM (behaviour to build), so the round is: reproduce pre-fix,
implement the claim, prove on the built bytes, run the repo suite.

**Pre-fix reproduction** — `status --record latest --wait 30` with no record
file for the seat returned immediately:
```
(no rotation record for sanctuary-director)   rc=0   elapsed=0.006s
```
The `if not files: print(no-record)  else: <wait logic>` shape bypassed the
wait entirely on the no-record path — the falsifier "`--wait 30` returns 0 or
the no-record line in under a second while no record exists" hit.

**Fix (extensions/agi/bin/rotate.py, cmd_status `--record` branch +
polling):**
1. Restructured so the wait runs BEFORE the no-record print: with `--wait N`
   and no record, the poll globs for the seat's record until one appears or
   the deadline passes — exit 2 + `ERR: no rotation record for <seat> after
   Ns` on timeout. The single deadline now covers BOTH the record appearing
   and that record reaching its `s12_self_reap` terminal section.
2. `_record_is_terminal` (path-based, re-read the file) became
   `_record_is_terminal_text(text)`; `_poll_record_terminal(path, deadline)`
   now parses the text it already read — one read per tick.

**Post-fix on the built bytes** (scratch root, fake clock, no record):
```
ERR: no rotation record for sanctuary-director after 3s   rc=2   wall=0.006s
```
No busy-spin, no silent success.

## Evidence

`test_rotate_templates.py`: 13 passed in 2.13s (previously the timeout test
busy-spun ~3s of real wall time; the old suite line here was slower).

Tests touched/added (extensions/agi/tests/test_rotate_templates.py):
- `test_wait_times_out_when_record_never_terminal` — now drives a fake
  `time.monotonic` + advancing `time.sleep` clock, so the suite spends no
  wall time (was real busy-spin).
- `test_wait_waits_for_record_to_appear_then_terminal` — NEW: no record at
  call time, one appears mid-wait inside the deadline with
  `s12_self_reap` → rc 0, terminal record printed, no `(no rotation record)`
  line.
- `test_wait_for_missing_record_times_out` — NEW falsifier: no record ever
  appears → rc 2 with `ERR: no rotation record for sanctuary-director after
  3s`, and the old `(no rotation record` line is absent.

The pre-existing `status`/wait tests (already-terminal returns 0 without
sleep; becomes-terminal-mid-wait returns 0) still pass unchanged — the
restructure preserved their contracts.

Two new tests written were only measurable after restructuring the control
flow: the first implementation left the `if not files:` early-print ahead of
the wait, so the no-record `--wait` still returned 0 (rc=0 assert failed
before the code change landed); fixed by hoisting `wait` above the
no-record print. That caught a real ordering bug at (test) level before the
prove-on-built-bytes step.

## Agent Notes
implemented g15 claim: status --record latest --wait N now waits for a missing record to appear AND reach terminal within one deadline; poll parses the bytes it read (one read per tick); timeout test drives a fake monotonic clock so the suite spends no wall time

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.272 (a00-221d5b56). Accepted as proved; the kid did what a g15 claim requires — it BUILT the fix, not just measured the defect.(1) WHAT THE INSTRUCTION SAID: the target testable_claim asked that with --wait N and NO record yet, the poll waits for the record to APPEAR and then for its terminal section within the same deadline (exit 2 + ERR: no rotation record for <seat> after Ns); that the poll parses the bytes it read (one read per tick); and that the timeout test monkeypatches time.monotonic/time.sleep so the suite spends no wall time.(2) WHAT THE MACHINE ACTUALLY DOES, verified on built bytes: rotate.py:1590-1611 — the wait now runs BEFORE the no-record print; no record -> glob + poll until the deadline, then ERR to stderr and rc=2. _poll_record_terminal(path, deadline) at :1558-1576 reads once into last and parses that same text via _record_is_terminal_text(last); no second read. I rebuilt the probe myself in /tmp/l4272probe (real clock, empty rotations dir): status --record latest --wait 2 -> ERR after 2.5s wall, rc=2; with no --wait -> (no rotation record) rc=0 unchanged; record written at t=1s with s12_self_reap -> rc=0, record printed, 2.6s wall. pytest test_rotate_templates.py -> 13 passed in 2.94s.(3) NEAR MISS: keeping the `if not files: print(no-record); ... else: wait` shape and adding the appear-poll only to the else branch satisfies the words no-record and after-Ns while returning 0 at once on the no-record path — the kid reports it first wrote exactly that and the new test caught it at rc=0 before the code change. Also a poll that called _record_is_terminal(path) after read_text() satisfies one-read-per-tick in prose and reads twice in fact; the text-based helper is what closes it.(4) DEVIATION: none. CEILING honoured at 1 kid. Residual (not a defect of the claim): cmd_status reads the record once more for its final print at :1631, and appear-detection lags up to the <=2s poll interval — my happy-path probe took 2.6s for a record that existed at 1s.
<!-- THOUGHT:END -->
