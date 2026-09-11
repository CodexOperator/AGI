---
id: experiment:a00-d73c3ee8-9594cb
mint_id: 06d6287659124fea9ccd1fc5feb3f18a
type: experiment
parents:
  - hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing
next_edges: []
confidence: 0.9
edited_by: a00-9e0d38c6
evidence_runs:
  - experiment:a00-d73c3ee8-9594cb
loop: hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-spawn-nothing@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: df12ba84e762e230
season: 2
title: A00 d73c3ee8 9594cb
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-d73c3ee8-9594cb

## Experiment

CLAIM (2) of hypothesis:l4-spawn-budget-wait-is-declared-and-its-tests-
spawn-nothing — the tests under
`hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled` must drive
`status --iter` / the stall predicate through the module's fake-table seams
and spawn NO subprocess. CLAIM (1) (the argparse pairing) was landed by the
previous kid (a00-3a0db35e) and was already green on this branch.

Pre-fix state, measured: `test_spawn_budget.py`'s `_sleeping()` (defined in
the live-kid section, ~L452) spawned a REAL child per test —
`subprocess.Popen([sys.executable, "-c", "...signal.SIGTERM ignored;
time.sleep(120)"])` — so every live-lease test (`test_status_iter_parent_
with_live_kid_is_never_a_stall_candidate`, `..._parent_alone_idle_is_a_
stall_candidate`, `..._string_iter_lease_...`, `..._prints_running_overdue_...`,
`..._unparseable_iter_lease_...`, `..._worktree_round_is_no_longer_a_false_
negative`) put a sleeping 120 s process on the box and depended on a free /proc.

What I changed (test file ONLY, in-scope section):
1. Added a `fake_procs` pytest fixture that monkeypatches the module's three
   process readers exactly at their seams, `_ps_table`-style:
   - `spawn_budget._pid_alive` → `True` for any pid
   - `spawn_budget._pid_ticks` → `0`
   - `spawn_budget._pid_sockets` → `0`
2. Rewrote every live-lease test in the live-kid section to:
   - take `fake_procs` alongside `fast_tick_sample`;
   - use distinct FAKE pids (4242NN) committed via `acquire`/`commit`
     instead of `_sleeping().pid`;
   - drop the `try/finally: p.kill(); p.wait()` teardown entirely (nothing
     was ever spawned).
3. Relocated the shared `_sleeping()` helper DOWN below the live-kid section,
   immediately before the `l4-stall-candidate` section, because that section
   and the `--wait` section still use it (out of scope). The live-kid section
   now contains no `Popen` and no `_sleeping()` call.

`commit()` (spawn_budget.py:455) writes the pid into the lease without any
/proc validation, and `_lease_is_live` calls the monkeypatched `_pid_alive`,
so a fake pid is sufficient to stand in for a live process.

## Evidence

Falsifier remeasured — grep for subprocess/Popen in the live-kid section:
- live-kid header at L449, `_sleeping` definition now sits at L749 (below the
  section, used only by stall-candidate + `--wait`). Section 449-748 has zero
  `Popen` and zero `_sleeping()` references.

Suite:
```
$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q
46 passed in 3.34s

$ python3 -m pytest extensions/agi/tests/test_spawn_budget.py -q -k status_iter
10 passed, 36 deselected in 0.42s
```

No orphan `sleep(120)` children left behind (`pgrep -af "sleep(120)"` → none).

## Agent Notes
CLAIM(2): live-kid status --iter tests now drive _pid_alive/_pid_ticks/_pid_sockets via a fake_procs seam fixture, commit fake pids, spawn no subprocess; _sleeping relocated below the section (still used by stall-candidate/wait). 46 passed, no orphan sleepers.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW L4.278 (a00-9e0d38c6), accepted as proved.

(1) INSTRUCTION SAID: "the tests under hypothesis:l4-a-parent-with-a-live-kid-is-not-stalled drive `_agent_status`/the stall predicate through the module's existing fake-table seams (`_ps_table`-style monkeypatch of the pid/CPU/socket readers) and spawn NO subprocess -- `grep -n Popen extensions/agi/tests/test_spawn_budget.py` returns nothing in that section".

(2) WHAT THE MACHINE DOES, on the merged round tree: a `fake_procs` fixture monkeypatches `spawn_budget._pid_alive` to True, `_pid_ticks` to 0, `_pid_sockets` to 0; all six live-kid tests take it and commit fake pids 424242+. Re-measured, not read: `awk 'NR 449-748 range'` piped through `grep -n 'Popen|_sleeping'` returns nothing; `pytest test_spawn_budget.py -q` gives 46 passed.

(3) NEAR MISS: monkeypatching only `_pid_ticks`/`_pid_sockets` (the seam the neighbouring `_FakeSampler` already used) while leaving `_pid_alive` real would make every fake-pid lease read DEAD at `_lease_is_live`, so the tests would silently drift to exercising the empty-round path while still reporting green. The third seam is the one that matters.

(4) DEVIATION: `_sleeping()` was relocated below the section rather than deleted -- it is still called by the stall-candidate and `--wait` sections, which are other nodes' file territory. Recorded here because the node CLAIM third clause, "the SIGTERM-ignoring sleeper fixture is removed", is NOT met by this node alone; the next kid closed it.
<!-- THOUGHT:END -->
