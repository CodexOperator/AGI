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

## ORDERS (kid, DG1.07) -- the round has NO parent: ONE kid does the whole fix (a claude-code parent cannot dispatch below ladder tier 3: claude_code_adapter.py:439-448)
BASE      CUT FROM de-base-pid tip 4d4c94b59 (worktree .agi/worktrees/de-base-pid). No merge. Never rebase.
1. MEASURE FIRST: which of the 12 hard-coded 4242 hits in extensions/agi/tests/test_dispatch.py reach spawn_budget._pid_alive (directly, or through dispatch / the reaper / a lease)? Paste a table: file:line -> reaches liveness yes/no, and HOW you know (a stub, a traceback, or reading the call). Only the yes rows change.
2. FIX the yes rows with ONE small helper in test_dispatch.py: a pid proven dead at test time (spawn a short child, wait it, use its pid; or a pid above int(open('/proc/sys/kernel/pid_max').read()); or a stubbed liveness seam). Never a hard-coded small pid, never kill or signal a pid that is not your own child.
3. PROVE: (a) on the untouched trunk bytes, with a live thread pid substituted for 4242 (a sleeping child of the test, or _pid_alive stubbed True for 4242), the named test test_two_parents_keep_separate_orders_copies_in_one_iter_dir goes RED -- paste the run; (b) with your fix the same forcing leaves it GREEN -- paste the run; (c) test_dispatch.py whole file green, twice in a row. Run named files under timeout, never a bare-dir pytest.
4. OPTIONAL, MEASURE ONLY, no code: does _pid_alive read a thread id as a process (/proc/<tid>/stat exists for TIDs, os.kill works on them)? One paragraph on the experiment node: should a pid with Tgid != Pid read dead, and can any lease legitimately hold a non-leader pid? A spawn_budget.py change is a separate leaf, never this round.
SAFETY    NEVER find / grep -r outside your own worktree; never walk .agi/worktrees or /mnt/agi-ram; git grep -- <paths> only. COMMIT every edit on the branch BEFORE you run cli.py done, and check git status -s after.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
FILE SCOPE extensions/agi/tests/test_dispatch.py (+ at most the ONE other test file / conftest helper step 1 names) · your own kid node. NEVER extensions/agi/bin/spawn_budget.py or any production file.
CEILING   HARD CAP: 1 kid, 0 parents · 0 production lines · 40 test lines · claude-code Sonnet (kid model cell) · 0 USD beyond the lane -- a byte or kid over it = the round is cut

## ORDERS (kid, DG1.08) -- SECOND kid round (DG1.07 a00-5118dcab measured line 2769 as the one yes row, applied nothing: its pytest wrappers were denied). Replaces the DG1.07 orders; same FILE SCOPE, SAFETY, ANON, CEILING.
BASE      CUT FROM de-base-pid tip b60a9a2e4 (worktree .agi/worktrees/de-base-pid). No merge. Never rebase.
RUN RULE  run tests ONLY as a BARE command from your own cwd: `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k two_parents_keep_separate` -- no env prefix, no timeout, no pipe, no redirect, no cd out of your checkout. If a bare pytest is STILL denied, say so on your experiment node (one line), apply the fix anyway, and stop: the director runs the proof.
1. RUN the named test once, bare, BEFORE editing: on this box pid 4242 is a live thread (/proc/4242/status Tgid 4238), so it should be RED (assert 1 == 2). Paste the result either way (if it is green, say so: the box changed).
2. APPLY the fix at test_dispatch.py:2769 only (DG1.07's static read: the only 4242 that reaches spawn_budget._pid_alive via Popen pid -> lease -> second acquire): replace the hard-coded 4242 by the pid of a child this test spawned and REAPED (or int(open('/proc/sys/kernel/pid_max').read()) + 1, which needs no process: pick ONE, name it in a comment). One small helper in the file, <= 40 test lines. Do NOT touch the 8 _FakeAdapter(pid=4242) rows (they only record the pid; DG1.07 found no liveness read) unless step 3 shows one red.
3. RUN bare: the named test again (must be GREEN), then `python3 -m pytest extensions/agi/tests/test_dispatch.py -q` whole file (green). Paste both.
4. Commit nothing by hand (your tool list denies git commit): cli.py done lands the dirty tree; check git status -s after. Optional step of DG1.07 (thread id read as a process) stays MEASURE ONLY, one paragraph, no code.

## ORDERS (text-fix kid, DG1.09) -- closes mur dg1pid-c1 R1: ONE code COMMENT, no logic
BASE      CUT FROM de-base-pid2 tip 9ef83c5f6 (worktree .agi/worktrees/de-base-pid2). No merge. Never rebase.
1. extensions/agi/tests/test_dispatch.py, the 3-line comment just above `pid = int(open("/proc/sys/kernel/pid_max").read()) + 1` (class _Proc, in test_two_parents_keep_separate_orders_copies_in_one_iter_dir, ~:2769-2771) states the mechanism INVERTED: it says _pid_alive reads the lease live "only via the fake poll()"; _pid_alive never calls poll() (spawn_budget.py:384-418). REPLACE exactly those comment lines by (<= 79 columns each): "# pid_max + 1 is never allocated by the kernel, so spawn_budget._pid_alive" / "# reads this lease DEAD: the first parent's slot is freed and the second" / "# parent is admitted at DEFAULT_MAX_LIVE = 1. A hard-coded 4242 is a live" / "# thread on some boxes: the lease then reads live and the 2nd dispatch is refused." (wrap the last line to 79 columns). The code line below the comment stays BYTE-IDENTICAL; touch nothing else.
2. Run nothing that is denied. If a BARE `python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k two_parents_keep_separate` runs, paste it (expected 1 passed); if denied, say so in one line on your experiment node. The director re-proves.
SAFETY    NEVER find / grep -r outside your own worktree; never walk .agi/worktrees or /mnt/agi-ram; git grep -- <paths> only. cli.py done lands the dirty tree (your tool list denies git commit).
ANON      no user name, home or repo path value, host or IP.
FILE SCOPE extensions/agi/tests/test_dispatch.py (the comment lines only) · your own kid node. NEVER a production file, never the code line.
CEILING   HARD CAP: 1 kid, 0 parents · 0 production lines · 0 code lines changed (comment only, <= 5 lines) · claude-code Sonnet (kid model cell) -- a byte or kid over it = the round is cut
