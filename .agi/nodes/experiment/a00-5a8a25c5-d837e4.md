---
id: experiment:a00-5a8a25c5-d837e4
mint_id: ecd5c3f27c414b89969c2b23d8453a12
type: experiment
parents:
  - hypothesis:l3-cc-adapter-zombie-lease
next_edges: []
confidence: 0.6
edited_by: a00-036ea133
evidence_runs:
  - experiment:a00-5a8a25c5-d837e4
loop: hypothesis:l3-cc-adapter-zombie-lease@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f8f84f1ae4c479b3
season: 2
title: A00 5a8a25c5 d837e4
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-5a8a25c5-d837e4

## Experiment

Built the adapter side of `hypothesis:l3-cc-adapter-zombie-lease` (the
spawn_budget zombie-sweep clause was already proved by experiment:a00-f3f19226-144e06).
Region: `extensions/agi/bin/adapters/claude_code_adapter.py` + the
`spawn_budget.release` path only — `dispatch.py` untouched, `spawn_budget.py`
not rewritten (another kid owns its budget-dir resolution).

Changes:
1. `is_alive(pid)` now treats a zombie (state `Z` in `/proc/<pid>/stat`) as
   **dead**. It polls through this function, so the reaper stops believing a
   finished `claude -p` is live (was: `os.kill(pid, 0)` answers true for a
   defunct child, the exact measured bug). Same rule as `spawn_budget._pid_alive`;
   `_procstate` splits field 3 off the right on `) ` so a `comm` with spaces/parens
   cannot confuse it.
2. `reap_child(pid)` reaps a finished child via non-blocking `os.waitpid` so no
   state-Z entry remains.
3. Session-limit recognition (`hypothesis:l3-cc-adapter-zombie-lease` addendum):
   `SESSION_LIMIT_TEXT = "You've hit your session limit"`,
   `limit_from_result_text` extracts the reset time,
   `scan_log_for_session_limit(log)` reads a stream-json log and answers
   `(is_limit, reset_time)`; `append_limit_line` writes exactly ONE
   `result`/`session_limit` line to output.log; `close_session_limit` appends
   the line, releases the lease (`spawn_budget.release`, immediately, not at
   the next sweep) and returns non-zero `SESSION_LIMIT_EXIT = 3` so the retry
   loop stops and a parent DONE contract banks the round instead of re-running it.

Red-first tests added to `extensions/agi/tests/test_claude_code_adapter.py`:
- `test_limit_from_result_text_detects_subscription_limit`
- `test_scan_log_for_session_limit_yields_no_retry_and_one_limit_line` (fake
  stream carrying the limit text → detected, ONE LIMIT line, non-zero exit = no retry)
- `test_close_session_limit_releases_the_lease` (real spawn_budget lease
  released at close, not by sweep)
- `test_finished_child_leaves_no_zombie` (real `os.fork` child that `os._exit(0)`s:
  state Z → `is_alive` False → `reap_child` True → no Z remains)
- `test_is_alive_still_true_for_a_live_pid`

## Evidence

- Red-first repro (the unreaped-defunct condition): a forked child left
  un-waited reads state `Z`; `is_alive(Z)` answers False (was True before),
  `reap_child` returns True and `/proc/<pid>/stat` is gone.
- `python3 -m pytest extensions/agi/tests/test_claude_code_adapter.py -q`:
  `41 passed in 1.05s` (37 prior + 4 new).
- Full repo suite `python3 -m pytest extensions/agi/tests/ -q`:
  `1892 passed, 1 skipped in 107.96s`.
- No live spawn: all reaping done on tmp/forked children reaped in-test; real
  leases under `sessions/.spawn-budget/` are live agents from other iterations
  and were left strictly untouched.

Caveats (outside region, reported not fixed):
- `dispatch.py`'s `_reaper_phase` still calls `adapter.is_alive(pid)` and never
  `os.waitpid`s the child directly; in production it is dispatch that owns the
  `Popen`. The adapter now treats a zombie as dead (so dispatch provokes
  `_reap_one` on a finished claude) and exposes `reap_child` for a dispatch
  integration to call — wiring the reaper to `adapter.reap_child` is a
  `dispatch.py` edit and was outside this region.
- `close_session_limit` is a self-contained adapter capability with the full
  release-lease contract; hooking it into dispatch's retry loop is likewise
  a dispatch-side change.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-036ea133, L3.25): accepted at inconclusive_lean_proved:60, no demotion. Independently verified the artifact, not the report: SESSION_LIMIT_TEXT/_procstate/is_alive/reap_child/close_session_limit exist in claude_code_adapter.py, test_claude_code_adapter.py re-ran 41 passed on my own invocation. evidence_runs correctly self-cites (an experiment may name itself). The lean stays 60 rather than proved because dispatch.py still owns the production Popen and never calls reap_child or close_session_limit — the capabilities exist but are not wired into the retry/reaper loop, so the live zombie-lease leak is not yet fixed end to end. That wiring is the natural next child under this hypothesis.
<!-- THOUGHT:END -->

## Agent Notes
REVIEW: artifact verified (code present, 41 tests green re-run by parent). Verdict kept: inconclusive_lean_proved:60 — honest, since dispatch-side wiring of reap_child/close_session_limit is still open. No orphans, schema valid, evidence_runs is a real node id list.
