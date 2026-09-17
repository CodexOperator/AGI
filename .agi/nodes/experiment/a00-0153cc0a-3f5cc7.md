---
id: experiment:a00-0153cc0a-3f5cc7
mint_id: a7ce7625008a4031985772fa66cde8e2
type: experiment
parents:
  - hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-while-the-suite-lock-is-held
next_edges: []
confidence: 0.92
edited_by: a00-be5c5e6e
evidence_runs:
  - experiment:a00-0153cc0a-3f5cc7
line_ceiling: 20
loop: hypothesis:l4-the-grid-cron-evidence-gate-defers-its-main-tree-rewrite-while-the-suite-lock-is-held@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "grep SUITE_LOCK/verify-suite.lock in grid.py; awk ordering 903-926", "expected": "NO second lock parser in grid.py; verification.acquire_suite_lock called BEFORE evidence_gate.enforce_on_disk on cron path", "observed": "grep empty (one reader = verification.acquire_suite_lock); acquire at grid.py:914 precedes enforce_on_disk at :922 inside do_all non-session", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "parent-probes.py: foreign LIVE pid (sleep 300) writes verify-suite.lock, one unevidenced proved node, run commit --all subprocess", "expected": "node byte-identical, deferred line exact-once, refs/grid/node/<mint>==1; re-held under 2nd foreign pid -> still deferred, node still proved", "observed": "byte-identical=True deferred_line_x1=True refs_written=True; retick deferred_again=True node_still_proved=True", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent-probes.py: unlink the held lock, second commit --all (tick-not-skip)", "expected": "next tick demotes the unevidenced proved node to inconclusive_lean_proved:50, no deferral line", "observed": "demoted=True no_deferral_line=True", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent-probes.py: lock names a real dead pid (os.fork-exited), first commit --all", "expected": "stale lock never defers; demoted on the FIRST call, no deferral line", "observed": "demoted_first_call=True no_deferral_line=True", "result": "pass"}
production_lines: 18
profile: balanced
role: kid
scaffold_hash: 9c84bb6c0884824e
season: 2
title: grid cron evidence gate defers while suite lock held
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-0153cc0a-3f5cc7

## Experiment

BUILD ORDER (g15): implemented the claim on real bytes.

**Change** (`extensions/agi/bin/grid.py`, +18 lines, ceiling 20):
- Added `import verification` (# noqa: E402 -- acquire_suite_lock: the ONE suite-lock reader). No second lock parser anywhere.
- In `cmd_commit`, inside `if do_all and not session:`, BEFORE `evidence_gate.enforce_on_disk`, probed `verification.acquire_suite_lock(root)`. On `(path, None)` we took the window only to probe it -> `gate_path.unlink(missing_ok=True)` so our pid is never planted; on `(None, holder)` (live FOREIGN pid) print `evidence gate deferred: suite lock held by pid {holder}` to stderr (the cron log) and skip ONLY the gate; else the gate runs as today. The flock acquisition and the ref-write loop are untouched, so already-committed bytes still get their refs.

`acquire_suite_lock` internally computes `<groot>/sessions/verify-suite.lock` and a dead-pid lock is stale-broken inside it, so a stale lock never defers on the first call and `holder == os.getpid()` (self) reads as stale.

**Tests** (`extensions/agi/tests/test_grid_evidence_gate_defer.py`), fixture root, the held-lock test runs `commit --all` as a SUBPROCESS so the gate pid differs from the lock-writer's:
1. `test_held_lock_defers_rewrite_and_refs_still_write` — test's own live pid in the lock -> node byte-identical, deferred line printed EXACTLY once, `refs/grid/node/<mint>` version count == 1 (refs still written).
2. `test_deferral_is_a_tick_not_a_skip` — held -> deferred, node stays `proved`; lock removed -> next `commit --all` demotes to `inconclusive_lean_proved:50` with no deferral line.
3. `test_stale_dead_pid_lock_never_defers` — lock named by a real (fork-exited) dead pid -> demoted on the FIRST call.

The subprocess env strips the harness `AGI_*` project-root vars and the `agent-git` hooksPath config entries, else `find_project_root` re-resolves to the worktree (would refuse on the season branch).

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_grid_evidence_gate_defer.py -q
3 passed in 0.83s

$ python3 -m pytest extensions/agi/tests/test_grid.py extensions/agi/tests/test_evidence_gate.py -q
255 passed

held-lock run (subprocess):
  STDOUT: v1 node/h1...1 ; grid: 1 new version(s), ... 0 demoted by the evidence gate
  STDERR: evidence gate deferred: suite lock held by pid <testpid>
  node after: verbatim `proved`, byte-identical
  lock file still holds the test's pid (we never planted ours)

dead-pid run: node rewrote to `verdict: inconclusive_lean_proved:50` (demoted first call)

git diff --numstat -- extensions/agi/bin/grid.py  =>  18 added / 2 removed  (<= 20)
```

## Agent Notes
Implemented +18-line suite-lock deferral probe in grid.py commit --all (import verification, acquire_suite_lock probe before enforce_on_disk, unlink probe-only window, print deferred line once, gate skipped only). 3 subprocess tests pass: held lock defers + refs still written; removed lock demotes next tick; dead-pid lock demotes first call. prod lines 18/20.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-be5c5e6e, SM.88): the KID VERSION was the authored implementation plus the kid's own 3 subprocess tests. THIS VERSION adds the parent's independent negative probes, one per claim conjunct, recorded in probes:. The probes went adversarial beyond the kid's own: conjunct 1 wire — grep grid.py for a second lock parser (none; ONE reader verification.acquire_suite_lock) and confirm acquire_suite_lock @914 precedes enforce_on_disk @922 on the do_all non-session path — pass. conjunct 2 gate — lock held by a genuinely FOREIGN live pid (a sleep 300 background process, never the test's own, so the self-pid-stale branch in acquire_suite_lock cannot be doing the work): commit --all leaves the proved node byte-identical, prints the deferred line exactly once, refs still written; re-held under a second foreign pid still defers and the node stays proved — pass. conjunct 3 gate — lock freed, the next commit --all demotes the unevidenced node to inconclusive_lean_proved:50 with no deferral line (tick, not skip) — pass. conjunct 4 gate — lock names a real fork-exited dead pid: demoted on the FIRST call, no deferral line (stale never defers) — pass. Existing grid/evidence/verification suites: 303 passed, no regression. The implementation unobtrusively reuses verification.acquire_suite_lock and unlinks the probe-only window so its own pid is never planted in the suite lock. Verdict proved stands on the parent's probes.
<!-- THOUGHT:END -->
