---
id: hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread
mint_id: 149e5b08ed664a6b9e5bd25ad563b6da
type: hypothesis
parents:
  - goal:g1
next_edges: []
edited_by: director-general-1
model: claude-sonnet-5-5
role: director
scaffold_hash: 1318b3e4cf0db24f
season: 2
testable_claim: no test whose fake child pid reaches spawn_budget._pid_alive uses a hard-coded pid; each uses a pid proven dead at test time (reaped child, pid above pid_max, or a stubbed liveness seam), and the named test passes with 4242 live
title: "G1 quick fix: test_dispatch fake child pid 4242 is a live thread after the reboot, so the suite must not bet on a hard-coded pid being dead"
town: core
---
# hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread


## Measured
- 22:5xZ 10-01 (SM, then DG1 re-ran): `extensions/agi/tests/test_dispatch.py::test_two_parents_keep_separate_orders_copies_in_one_iter_dir` is RED ALONE on the pure trunk (708727845 here; bd35bb5f9 in SM's run): `assert 1 == 2` (the manifest holds 1 agent). Green in SM's 22:0xZ suite, 0 engine commits between: an ENVIRONMENT change.
- Cause (DG1, `/proc/4242/status` on this box at 23:1xZ): pid 4242 is now the live THREAD `V8Worker` of process Tgid 4238 (an MCP node process, after the 22:2xZ reboot). The fake child of the test is `pid = 4242`; `spawn_budget._pid_alive` (spawn_budget.py:384) opens `/proc/4242/stat` (it exists), answers alive, so the first lease holds and the second dispatch is "unadmitted: spawn budget full (1/1 live tree-wide)" at DEFAULT_MAX_LIVE = 1.
- `git grep -n "4242" -- extensions/agi/tests/test_dispatch.py` = 12 hits (pid=4242 / "pid": 4242 / pid = 4242 at :515 :533 :550 :567 :636 :659 :676 :697 :1537 :1670 :2514 :2769). Only the ones whose pid reaches `spawn_budget._pid_alive` can go red; the round MEASURES which (not all 12).

## CLAIM
No test in the suite bets on a hard-coded pid being DEAD: every fake child whose pid reaches `spawn_budget._pid_alive` (directly, or through dispatch / the reaper / a lease) uses a pid proven dead at test time (a reaped child's pid, or a pid above `/proc/sys/kernel/pid_max`, or a stubbed liveness seam), so the suite's result does not depend on which pids are alive on the box that runs it.

## Dispatch line
config-max: none / template-max: none / code: test files only (a small shared helper + its call sites); NO production change in spawn_budget.py.

## FALSIFIERS
1. With pid 4242 (or any hard-coded fake pid the round names) forced LIVE (a sleeping child of the test, or `_pid_alive` stubbed True for that pid), the fixed tests still pass; on the trunk bytes the named test goes red. A test that passes only while the pid happens to be dead -> false.
2. `git grep -n "pid=4242\|\"pid\": 4242\|pid = 4242" -- extensions/agi/tests` still shows a hit whose pid reaches `_pid_alive` without a dead-pid helper or a stub -> false (the round lists each hit and its verdict: reaches liveness yes/no, by file:line).
3. The suite files the round touched are green when run twice in a row, and green with a live pid 4242 present.

## TESTS
- The named test red then green by the falsifier-1 method (paste both runs). `test_dispatch.py` and every neighbour the round touched stay green; run named files under `timeout`, never a bare-dir pytest.
- OPTIONAL second conjunct (MEASURE ONLY, no code): does `_pid_alive` read a thread id as a process (`os.kill` and `/proc/<tid>/stat` both work on TIDs)? Say on the experiment node whether a pid with `Tgid != Pid` in `/proc/<pid>/status` should read dead, and whether any lease can legitimately hold a non-leader pid. A production change is a separate goal leaf, never this round.

## FILE SCOPE
extensions/agi/tests/test_dispatch.py (+ at most the ONE other test file / conftest helper the measurement names) · this node's kid node. Never extensions/agi/bin/spawn_budget.py. Never kill or signal a pid that is not the test's own child.

## CEILING
1 parent · kids <= 1 · 0 production lines · <= 40 test lines · Sonnet 5.5 lane (claude-code), regular review (never research-review) · SAFETY: never find / grep -r outside your own worktree, never walk .agi/worktrees or /mnt/agi-ram; git grep -- <paths> only; COMMIT every edit on the branch before you report.
