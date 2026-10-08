---
id: experiment:a00-a11948b7-780eed
mint_id: 1676d73f68764b619113e8a58ddf8d08
type: experiment
parents:
  - hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-a11948b7-780eed
loop: hypothesis:g1-test-dispatch-fake-pid-is-not-a-live-thread@s2
model: claude-sonnet-5-5
profile: balanced
role: kid
scaffold_hash: cdd59766fc46382d
season: 2
title: A00 a11948b7 780eed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a11948b7-780eed

## Experiment

Bare pytest and sed were denied in this sandbox, so no pre-fix RED and no post-fix GREEN were observed. Applied the fix at test_dispatch.py:2769: `_Proc.pid = int(open("/proc/sys/kernel/pid_max").read()) + 1`, with a comment. Production lines: 0. The director must run the proof.

## Evidence

The kid ran nothing (its tool list denied every test run). The PROOF below is the director's (DG1, 10-02, my own uid, detached trees, pid 4242 LIVE at the time: /proc/4242/status = Name V8Worker, Tgid 4238). The kid's open risk (a nonexistent pid reads DEAD, so the test could go red the other way) is the DESIGN of the fix: the test passes BECAUSE the first lease reads dead and frees its slot at DEFAULT_MAX_LIVE = 1, so the second parent is admitted (mur dg1pid-c1 reproduced it).

### Director proof (DG1, 10-02)
| run | result |
|---|---|
| base ca406870e: `pytest extensions/agi/tests/test_dispatch.py -k two_parents_keep_separate` | 1 failed (RED, `assert 1 == 2`, manifest holds 1 agent) |
| tip df60cf5a6, same test | 1 passed (GREEN) |
| tip, whole extensions/agi/tests/test_dispatch.py, twice | 139 passed, 139 passed |
| pid_max + 1 | a pid the kernel never allocates (pids are [1, pid_max - 1]): `/proc/<pid>/stat` absent, `os.kill` ESRCH, so `spawn_budget._pid_alive` reads it dead |

### Suite-wide probe (falsifier 2): which hard-coded fake pids reach `_pid_alive`
Method: a pytest plugin wrapped `spawn_budget._pid_alive` and logged every call that returned alive for a pid that was not our own descendant or direct child, over the 31 test files that import spawn_budget / _pid_alive (1,401 tests, base test_dispatch.py, 4242 live). Result: pid 4242 appeared ONLY in `test_two_parents_keep_separate_orders_copies_in_one_iter_dir` (2 hits); pid 1 only in `test_verification_window.py::test_window_names_the_registered_runner_behind_the_holder` (a deliberately ALWAYS-live holder: benign, it bets on ALIVE); every other hit is a real child process of `test_spawn_budget`'s concurrency test (by design).
| test_dispatch.py line (base) | what | reaches `_pid_alive` |
|---|---|---|
| 515 533 550 567 636 659 676 2514 | `_FakeAdapter(pid=4242)` | NO (probe: 0 alive-calls for 4242 in these tests while 4242 was live) |
| 697 | agent.json fixture, adapter `is_alive` stubbed | NO |
| 1537 1670 | `_Proc.pid`, adapter seam | NO |
| 2654 | `_rec_pid` assertion | NO |
| 2769 | `_Proc.pid` of the named test: Popen faked, lease committed, 2nd dispatch `acquire` -> `_lease_is_live` -> `_pid_alive` | YES (fixed: pid_max + 1) |
R3 (mur verify 'missed'): `dispatch.py` `_kid_account_floor_exemption` (reads `_pid_alive` on a manifest pid) returns None unless `AGI_AGENT_ID` is set in the environment AND names a manifest record; none of the 4242 rows sets it (the tests leave it unset by their own per-test delenv / stubs, not by a blanket strip of AGI_*; conftest pops only AGI_AGENT_SESSIONS_ROOT), so it is unreachable from them -- and the probe above confirms it empirically (it would have logged 4242 from any row had it been reached).
The 31 files at the tip: 11 failed = ws_raw_client x2 (test_commands_manifest), test_provisioning x7 (needs the MAIN .env, my uid cannot read it), test_rotate_handover x2 (the ANON tmp-user one); on the base the same files = those 11 + the named test = 12: the fix removes exactly one red and adds none.
Optional conjunct (thread id read as a process): MEASURED, no code: `/proc/<tid>/stat` exists for a thread id and `os.kill` accepts it, so `_pid_alive(4242)` reads a V8Worker THREAD as alive; whether `Tgid != Pid` should read dead is a production change for a separate leaf (a lease holds an agent's process-leader pid, so no legitimate lease should hold a non-leader pid).

## Agent Notes
fix applied at line 2769 (pid_max+1) by the kid; the kid ran no test (denied); PROVED by the director's runs above (RED on base, GREEN at tip, whole file 139 x2, suite-wide probe)
