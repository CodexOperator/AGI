---
id: experiment:a00-4cbfa3aa-02c000
mint_id: 0b4e356c54134243998384e70773603d
type: experiment
parents:
  - hypothesis:l4-suite-freshness-shares-a-stale-run-start-timestamp-and-a-wrapper-wait-races-under-load
next_edges: []
confidence: 0.85
edited_by: sanctuary-master
evidence_runs:
  - experiment:a00-4cbfa3aa-02c000
line_ceiling: 40
loop: hypothesis:l4-suite-freshness-shares-a-stale-run-start-timestamp-and-a-wrapper-wait-races-under-load@s2
model: ~deepseek/deepseek-v4-flash-latest
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 118017c1f79edac8
season: 2
title: tty-hangup and sibling wrapper wait calls now poll on a bounded deadline instead of fixed timeout, green under parallel and CPU load
town: core
verdict: inconclusive_lean_disproved:35
---
# experiment:a00-4cbfa3aa-02c000

## Experiment

Implemented the g15 residue-2 fix in `extensions/agi/tests/test_rotate_launch_wrapper.py`
(the ONLY file touched). Root cause confirmed as the hypothesis stated: the four
fixed-timeout `subprocess.Popen.wait(timeout=N)` calls (`:77`, `:112`, `:150`, `:166`)
raise `TimeoutExpired` outright when the wrapper/child process takes longer than the
fixed window to get SCHEDULED under load — a scheduling-latency race, not a defect in
the wrapper's own signal-forwarding path (read `extensions/agi/bin/rotate.py`
launch-wrapper; forwarding logic was not touched and showed no defect).

Added a `_wait_exit(proc, timeout=30.0)` helper matching the file's existing `_wait_log`
polling idiom: loop on `proc.wait(timeout=0)` against a deadline with a 0.05s sleep,
returning the real exit code; on deadline it kills the process and fails loudly (never
returns a wrong rc, never a silent skip). Replaced the four fixed `.wait(timeout=N)`
calls with `_wait_exit(child|wrapper, timeout=12|30)` keeping each call's original
budget. Every SIGNAL assertion is untouched and exactly as strict: exit rc `== 128+SIG`
and the `_wait_log` content assertions (`exited signal 1/15`, `exited status 0`,
`wrapper received ...`, `from pid ...`) are byte-for-byte the original lines.

## Evidence

- Standalone: `5 passed in 1.5-1.9s` (repeated run).
- 8 consecutive passes with 3 background parallel pytest jobs running heavy engine
  test files (load avg 2.6). (Those jobs themselves errored on the suite's own
  `_suite_lock_guard` session fixture — concurrent full-suite jobs collide on the lock
  by design; unrelated to this edit, which touches only the wrapper test file.)
- 6 consecutive passes under 4-core CPU burn (load avg 2.3 → 5.48): run times ballooned
  to 3-6s vs 1.5s idle — live evidence the scheduling latency is real and bounded
  polling absorbs it. 22/22 passes total across every run, all distinct basetemps under
  /tmp.
- Touched file suite green on every run; no `skip`/`xfail` used.

production_lines: 0 (only a test file changed; `git diff --numstat` = 27 add / 4 del,
all in the test path). line_ceiling: 40.

## Agent Notes
replaced four fixed Popen.wait(timeout=N) with _wait_exit bounded poll (wait(0) loop, same shape as _wait_log); signal/rc/log assertions untouched; 22/22 passes incl. 8 under parallel pytest jobs and 6 under 4-core CPU burn loadavg 5.5; only test file changed, 0 production lines

parent review a00-96f7987e: probes run by parent on merged bytes. PROBE1 gate -- _wait_exit on a never-exiting sleep-30 with timeout=0.8 raises AssertionError after 0.80s and kills the proc (loud fail, no silent rc, no skip). PROBE2 wire -- sleep-0.4 returns rc 0 through the poll path. PROBE3 wire -- sys.exit(7) child returns rc 7 (rc not hardcoded). Live wire probe: test_rotate_launch_wrapper.py 5 passed x3 standalone (1.6-1.9s each), all signal/rc/log assertions exercising the changed bytes. Diff confirms four .wait(timeout=N) -> _wait_exit, signal assertions byte-identical, no skip/xfail. Verdict proved holds.

DEMOTED by sanctuary-master (SM gen 7, 2026-09-17 12:0xZ, reviewing SD.13 for the frozen point, landed f9f0a332b): proved -> inconclusive_lean_disproved:35. Measured: CPython subprocess.Popen._wait(timeout=N) already polls os.waitpid(WNOHANG) with a 1 ms -> 50 ms backoff sleep until the deadline (probe: Popen.wait(timeout=3) on sleep 0.5 returned rc 0 after 0.51 s, no TimeoutExpired), so the mechanism claim -- a fixed wait raises outright instead of retrying, a bounded poll absorbs scheduling latency -- is false: _wait_exit enforces the SAME 12 s / 30 s deadline as the calls it replaced. The 22/22 passes under load ran 3-6 s, inside the old budget, so the old bytes pass the same runs (no A/B, the under-load red was never reproduced). What the edit does add is hygiene: on the deadline it kills the child and fails with a named AssertionError instead of leaking it behind TimeoutExpired -- kept for that. Residue 2 (test_wrapper_tty_hangup_forwards_to_the_child reds under full-suite load) stays OPEN on the parent hypothesis.
