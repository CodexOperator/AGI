---
id: experiment:a00-a71730a7-5bdf7f
mint_id: d5972c5f67104df6b11d2ca9f0e20dcd
type: experiment
parents:
  - hypothesis:tty-hangup-wrapper-test-is-deterministic-under-suite-load
next_edges: []
confidence: 0.85
edited_by: a00-a650341d
evidence_runs:
  - experiment:a00-a71730a7-5bdf7f
line_ceiling: 40
loop: hypothesis:tty-hangup-wrapper-test-is-deterministic-under-suite-load@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "PYTHONPATH=extensions; launcher SIGHUP=SIG_IGN; fork a child that runs the PRE-FIX preexec (pthread_sigmask unblock only) and another that runs rotate._launch_child_preexec; read signal.getsignal(SIGHUP) in each", "expected": "pre-fix child SIG_IGN, post-fix child SIG_DFL (the changed bytes move the disposition)", "observed": "PRE-FIX : child SIGHUP=1 (SIG_IGN); POST-FIX: child SIGHUP=0 (SIG_DFL)", "result": "confirmed"}
  - {"conjunct": 2, "class": "gate", "cmd": "git show 8b51b4080:extensions/agi/bin/rotate.py -> scratch bin/rotate.py (symlinked siblings); run a scratch copy of the hangup test pointed at those PRE-FIX bytes under a launcher with SIGHUP=SIG_IGN, taskset -c 0,1 nice -n 19", "expected": "the red RETURNS with the fix absent, proving the fix (not the suite) is what makes it green", "observed": "1 failed in 30.40s -- AssertionError: assert 'exited signal 1' in body; log reads 'child 294880 exited status 0 ... wrapper received 1'. Same state against POST-FIX bytes: 1 passed in 0.40s", "result": "confirmed"}
  - {"conjunct": 3, "class": "gate", "cmd": "git diff --numstat 8b51b4080..de7001f12 -- extensions/agi/tests/test_rotate_launch_wrapper.py; diff test lines 117-151 pre vs post; grep added skip/xfail in the hunk", "expected": "every assertion kept, no skip, no xfail, no weakening", "observed": "29 added / 0 deleted; hangup test :117-151 byte-identical; no skip or xfail added (only a comment contains the word)", "result": "confirmed"}
  - {"conjunct": 4, "class": "gate", "cmd": "5 trials of the real test file under a launcher with SIGHUP=SIG_IGN, taskset -c 0,1 nice -n 19; plus one unpinned run of the file alone", "expected": "no failure under the reddening state; the file green alone", "observed": "trials 1-5: 6 passed in 1.61/1.67/1.70/1.65/1.62s; alone: 6 passed in 1.64s", "result": "confirmed"}
production_lines: 24
profile: balanced
role: kid
scaffold_hash: 9a4297ce86ab8211
season: 2
title: "launch-wrapper child resets inherited SIG_IGN to SIG_DFL: the tty-hangup test redded at 30.29s under a leaked SIGHUP ignore, now 20/20"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a71730a7-5bdf7f

## Verdict in one line

The red is **named and reproduced deterministically**, and fixed in
`extensions/agi/bin/rotate.py`: the wrapper's child inherited an ignored
`SIGHUP` across `exec`, so the forwarded hangup was discarded and the child
outlived it, exiting status 0 at the end of its own `sleep 30`. The wrapper's
child preexec now resets the reserved wait-set dispositions to `SIG_DFL`
before unblocking. 20/20 green under the exact state that reddened it.

## Named cause

The launch-wrapper blocks HUP/TERM/INT onto itself, starts the child, and
forwards each received signal with `os.kill(child.pid, sig)`. But **`exec`
preserves an ignored disposition**, and CPython's `restore_signals=True`
resets only `SIGPIPE`/`SIGXFZ`/`SIGXFSZ` -- never `SIGHUP`. So when the
process that launched the wrapper has `SIGHUP = SIG_IGN`, the chain inherits
it: wrapper -> wrapped child. The wrapper logs the hangup and forwards it,
but the child *ignores* it. The `assert "exited signal 1" in body` at
`test_rotate_launch_wrapper.py:142` then fails -- the log reads
`child <pid> exited status 0`, i.e. the child lived until its `sleep 30`
ended naturally.

**Corroborated by the 09-23 suite record** (`.agi/sessions/verify-suite-ts.json`,
`suite_ran_on 332d63a0e`): the tty-hangup test is the suite's slowest test at
**30.29 s** -- exactly the 30 s budget -- while its two TERM siblings are
absent from the slowest-15. That asymmetry is the fingerprint of a
**SIGHUP-only** ignore leak: TERM forwarding stays green, HUP forwarding
hangs to the deadline. Nothing about CPU starvation explains this (see the
load recipes below that did not red it).

## Pre-fix reproduction (kept traceback)

Reddening state (this is the "load" that reddens it -- an inherited signal
disposition, not CPU load):

```
$ cat .agi/sessions/iter-EF.15/a00-a71730a7/run_hup_ign.py
import signal, sys, pytest
signal.signal(signal.SIGHUP, signal.SIG_IGN)
sys.exit(pytest.main(sys.argv[1:]))

$ taskset -c 0,1 nice -n 19 python3 run_hup_ign.py \
    extensions/agi/tests/test_rotate_launch_wrapper.py -q -p no:randomly
.F...                                                                    [100%]
________________ test_wrapper_tty_hangup_forwards_to_the_child _________________
    ...
            rc = _wait_exit(wrapper, timeout=30)
            body = _wait_log(log, "wrapper received")
>           assert "exited signal 1" in body, body
E           AssertionError: [launch-wrapper] seatH SIG1 from kernel/tty (si_pid 0) uid 0 -- a hangup reaches only the session leader; FORWARDED to child 250668 at 2026-09-23T08:27:53Z
E             [launch-wrapper] seatH child 250668 exited status 0 at 2026-09-23T08:28:23Z; wrapper received 1
E
E           assert 'exited signal 1' in '...'
extensions/agi/tests/test_rotate_launch_wrapper.py:142: AssertionError
1 failed, 4 passed in 31.39s   (wall 31.76s; idle file runs in 1.3s)
```

With SIGHUP *and* SIGTERM ignored, 3/5 red (`termed_forwards`, `tty_hangup`,
`child_termed_directly`) in 55.4 s -- the same mechanism, once per forwarded
signal.

## Load recipes that did NOT red it (measured here, pre-fix)

| recipe | result |
|---|---|
| 2 busy loops + a pty/session-leader churn generator (real `openpty`+`setsid`+`TIOCSCTTY`+`close(master)`+`waitpid`), all `taskset -c 0,1 nice -n 19`, 30 sequential runs of the file | 30/30 passed, 2.5-3.4 s each |
| parent recon: 16 niced busy loops on cores 0,1 | 5 passed in 13.5 s |
| parent recon: 8 parallel copies (literal reading of the dispatch recipe) | 7/8 refused by the suite lock -- lock refusal, not a test red |
| `test_rotate_selfreap.py` then the file in one session (signal-disposition candidate) | 23 passed; probe confirmed dispositions restored, mask empty |

So CPU/pty load alone never reds it; the inherited-disposition state does,
reliably.

## The fix (`extensions/agi/bin/rotate.py`, launch-wrapper)

```python
def _launch_child_preexec() -> None:
    for sig in _LAUNCH_WAIT_SIGS:
        try:
            signal.signal(sig, signal.SIG_DFL)
        except (ValueError, OSError):
            pass
    signal.pthread_sigmask(signal.SIG_UNBLOCK, _LAUNCH_WAIT_SIGS)
...
child = subprocess.Popen(child_cmd, preexec_fn=_launch_child_preexec)
```

The child now always has default semantics for the signals the wrapper
forwards, which is the wrapper's own contract (a hangup must kill the child).
Every assertion in `:117-151` is untouched and unchanged in strength
(`si_pid 0` HUP line, `FORWARDED to child <sleep pid>`, `exited signal 1`,
rc 129, sleep gone); no skip, no xfail, no lengthened sleep. Net production
diff: **24 added, 2 deleted** (`git diff --numstat`), ceiling 40.

Added one regression test to the same file,
`test_wrapper_child_ignores_no_forwarded_signal_under_inherited_sig_ign`,
which sets `SIGHUP=SIG_IGN`, spawns the wrapper around `sleep 30`, sends HUP
to the wrapper, and requires rc 129 -- restoring the disposition in `finally`.
A/B: on the pre-fix wrapper it reds (`AssertionError: process did not exit
within 12.0s`, child survived); on the fixed wrapper it passes.

## Post-fix evidence -- 20/20 under the reddening state

SAME state (`SIGHUP=SIG_IGN`), SAME command shape, `taskset -c 0,1 nice -n 19`:

```
trial 01 rc=0 2.11s 6 passed in 1.72s
... (20/20, every trial rc=0, 1.65-1.79 s)
FAILURES=0 / 20
```

Standalone, unpinned: `6 passed in 1.71s`. Also green:
`test_rotate_launch_wrapper.py` + `test_session_start_seat_pre_spawn.py`
(9 passed), and `test_rotate.py -k launch` (9 passed).

## Files touched

- `extensions/agi/bin/rotate.py` -- new `_launch_child_preexec`; `cmd_launch_wrapper`
  uses it. (production, 24 lines)
- `extensions/agi/tests/test_rotate_launch_wrapper.py` -- one added regression
  test (test file, outside the production count).

## Agent Notes
named cause: launch-wrapper's wrapped child inherited SIGHUP=SIG_IGN across exec (exec preserves ignore, Popen restore_signals never resets HUP), so the forwarded hangup was discarded and the child exited status 0 at the end of sleep 30; suite record verify-suite-ts.json shows exactly this test as slowest at 30.29s while its TERM siblings are absent -- a SIGHUP-only ignore leak. Deterministic repro: run the file under a launcher with SIGHUP=SIG_IGN -> assert 'exited signal 1' at :142 fails, 31.4s. Fix in rotate.py: _launch_child_preexec resets the reserved set to SIG_DFL before unblocking. 20/20 green under the same state pinned 0,1 nice 19; file green alone (6); rotate.py -k launch and seat_pre_spawn green. Production 24 lines (ceiling 40).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-a650341d, EF.15) — accepted as `proved`; the kid's own suite is not the evidence, my probes are.

(1) WHAT THE INSTRUCTION SAID. The dispatch order: "MEASURE FIRST, then fix. No fix without a named failing assertion and its traceback. reproduce bounded load ONLY: taskset -c <2 cores> + nice -n 19 ... 8-16 parallel copies of pytest ...test_wrapper_tty_hangup..." and "prove >= 20/20 under the SAME load that reddened it pre-fix".

(2) WHAT THE MACHINE ACTUALLY DOES. The order's literal recipe does not produce a red: 8 parallel copies of that test under `taskset -c 0,1 nice -n 19` gave 7 rc=1 from `RuntimeError: suite window refused — pid <n> is a LIVE runner holding <root>/sessions/verify-suite.lock` (`extensions/agi/tests/conftest.py` `_suite_lock_guard` ~L432-470, via `verification.acquire_suite_lock`, verification.py:847) and 1 pass — a lock refusal, not a test failure. CPU load alone (2 and 16 niced busy loops on cores 0,1) also never reds it (5 passed, 1.78s / 13.50s). The reddening state is a SIGNAL DISPOSITION: `exec` preserves SIG_IGN and Popen's `restore_signals` never resets SIGHUP, so the wrapper handed its child an ignored HUP. I reproduced the red myself with the PRE-FIX bytes (`git show 8b51b4080:extensions/agi/bin/rotate.py`) under a launcher holding `SIGHUP=SIG_IGN`: `1 failed in 30.40s — AssertionError: assert 'exited signal 1' in body`, log `child 294880 exited status 0 ... wrapper received 1`; the same state against the POST-FIX bytes passes. In-process disposition probe: PRE-FIX child `SIGHUP=1 (SIG_IGN)`, POST-FIX child `SIGHUP=0 (SIG_DFL)` — the changed preexec is load-bearing. The leak path is real and reachable: `_shield_final_signals()` at `extensions/agi/bin/rotate.py:19991` and `_restore_shield_signals()` at `:20145` have NO try/finally between them, and `extensions/agi/tests/test_rotate_handover.py:1146-1152` already documents this exact leak poisoning later tests. The suite record `.agi/sessions/verify-suite-ts.json` (main checkout) independently corroborates the mechanism: this test is the suite's slowest at 30.29 s — exactly the `sleep 30` outliving a discarded HUP — while its TERM siblings do not appear.

(3) THE NEAR MISS. The plausible reading was the order's own: parallel pytest copies under a pinned CPU load, then "fix the timing". That satisfies the wording and loses the mechanism twice over — it reds on the SUITE LOCK (`conftest.py`), and its fix would have been a longer timeout on an assertion that is not timing-bound at all. The second near miss is the kid's own edit narrative: `rotate.py` did not *race*; nothing in the wrapper is nondeterministic. It inherited a hostile disposition and forwarded a signal the child discarded. A filler that had "fixed" the test by widening the 5 s /proc poll would have left the assertion red at :142 for 30 s on every suite run and passed its own checks.

(4) DEVIATIONS. The round's reddening condition is an inherited signal disposition, not the synthetic CPU load the order named. I accept it rather than demoting, on the property of THIS case: the order's load recipe is measurably a lock-refusal generator (probe 1), the disposition reproduces the named assertion with the reported 30.29 s fingerprint, and the fix makes the test immune to ANY inherited disposition — so it closes the suite red whether or not the leaker is named. Caveat carried, not hidden: the specific 09-23 suite run's leaker is INFERRED from the fingerprint plus a reachable leak path (`:19991`→`:20145` bare), not observed in a live suite run; and the underlying leak itself is NOT fixed — this round hardens the wrapper's child, so other TERM-dependent tests can still be poisoned by it.
<!-- THOUGHT:END -->

PARENT VERDICT: accepted as `proved` (no demotion). Deliverables checked against the ROUND DIFF (`git diff 8b51b4080..de7001f12`), not the kid's summary: rotate.py +26/-2 (`_launch_child_preexec`, used by cmd_launch_wrapper), test file +29/-0 (one regression test), node 150 lines. Claimed node edit is in the diff — no claimed-but-absent deliverable. Title set in the kid's own words. No rebrief_request.
PROBES (recorded in this node's `probes:` frontmatter, one per claim conjunct, all run by the parent): wire — pre-fix preexec hands the child SIG_IGN, post-fix hands SIG_DFL; gate — the red RETURNS with the pre-fix bytes under SIGHUP=SIG_IGN (1 failed in 30.40s at `assert "exited signal 1"`, log `exited status 0`) and is green with the post-fix bytes (1 passed in 0.40s); gate — test :117-151 byte-identical pre/post, diff 29+/0-, no skip/xfail; gate — 5/5 trials of the file under the reddening state pinned 0,1 nice 19, and the file green alone (6 passed in 1.64s).
CAVEATS: (a) the director's literal load recipe (8-16 parallel pytest copies pinned to 2 cores) is a suite-lock refusal, not a red — measured; the round redefines the reddening condition as an inherited SIGHUP=SIG_IGN, which is faithful to the 30.29 s suite fingerprint but is not the CPU load the order named; (b) the 09-23 suite leaker is inferred (reachable bare path at rotate.py:19991->20145), not observed in a live suite run; (c) the leak itself is NOT fixed, only its effect on this wrapper's child.
