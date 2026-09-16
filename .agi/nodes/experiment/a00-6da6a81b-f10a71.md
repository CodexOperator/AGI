---
id: experiment:a00-6da6a81b-f10a71
mint_id: cd49d99d41b54b6cb70a6be0d03c3273
type: experiment
parents:
  - hypothesis:l4-window-names-the-suite-lock-holder-pid-tree-age-command-and-runner-row-in-one-line
next_edges: []
confidence: 0.9
edited_by: a00-09301626
evidence_runs:
  - experiment:a00-6da6a81b-f10a71
line_ceiling: 35
loop: hypothesis:l4-window-names-the-suite-lock-holder-pid-tree-age-command-and-runner-row-in-one-line@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe (REAL /proc, no fixture): live `sleep 120` spawned with cwd=<main>/.agi/worktrees/post-foo, its pid written into sessions/verify-suite.lock with mtime now-42s, then verification.render_window(groot) in-process", "expected": "ONE lock line carrying the pid, `age 42s`, `tree post-foo`, `cmd sleep 120`", "observed": "lock: held by <pid> since <HH:MM:SSZ> (age 42s, tree post-foo, cmd sleep 120 ...) -- 1 lock line; probe file probe_window_holder.py::test_probe_c1_live_holder_in_worktree_names_tree_age_cmd + ::test_probe_c1b_exactly_one_lock_line PASS", "result": "pass"}
  - {"conjunct": 2, "class": "wire", "cmd": "parent probe: monkeypatch spawn_budget.live_leases_readonly to return one fabricated row keyed on the live holder's pid, then render_window; and a second probe writing a lease whose agent_pid/holder_pid are a DEAD pid", "expected": "the fabricated row SURFACES as `runner <agent_id> tier=<t> iter=<i>` (proves the call site goes through the budget reader), and a dead lease is NOT named", "observed": "runner a00-wire-only tier=parent iter=SM.65 present on the line; dead-lease probe line carries no `runner ` clause -- probe_window_holder.py::test_probe_c2b_runner_row_comes_through_spawn_budget_reader + ::test_probe_c2c_dead_lease_is_not_named PASS", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "parent probe (REAL /proc): lock names pid 2 (kthreadd -- alive to os.kill but /proc/2/cwd is EACCES), and lock names 999999999 (no such process); render_window must not raise in either case", "expected": "unreadable-but-alive holder degrades to today's line + `unresolved`; a dead pid keeps the stale-lock path `lock: free`; no traceback", "observed": "pid 2 -> `lock: held by 2 since ... (age 5s, tree unresolved, cmd ...)` no exception; pid 999999999 -> lock line exactly `lock: free` -- probe_window_holder.py::test_probe_c3b_unreadable_proc_degrades_unresolved + ::test_probe_c3_dead_pid_stays_free_unchanged PASS", "result": "pass"}
  - {"conjunct": 4, "class": "gate", "cmd": "parent probe: render_window on a fixture groot with NO lock file, and a second asserting the free line gains no enrichment token", "expected": "the lock line is byte-identical to today: exactly `lock: free`, no age/tree/cmd appended", "observed": "lock lines == ['lock: free']; `age`/`tree`/`cmd` absent from the free line -- probe_window_holder.py::test_probe_c4_free_line_byte_identical + ::test_probe_c4b_free_line_never_gains_age_tree_cmd PASS", "result": "pass"}
production_lines: 66
profile: balanced
role: kid
scaffold_hash: 1f99d1fb86d56401
season: 2
title: Window names the lock holder pid age tree cmd and runner row in one line
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-6da6a81b-f10a71

## Experiment

BUILD ORDER, not a measurement: implement the four conjuncts of
`hypothesis:l4-window-names-the-suite-lock-holder-pid-tree-age-command-and-runner-row-in-one-line`
on the real bytes, then prove them.

Pre-fix state, measured (scratch probe on a fixture groot holding a live pid):

```
PRE-FIX held line: lock: held by 1168186 since 19:04:19Z
PRE-FIX free line: lock: free
```

No pid-adjacent detail at all: no age, no tree, no command, no runner row.
One line was the whole payload a rotating seat got, so the holder had to be
identified by hand (`cat` the lock, `ps -p`, `readlink /proc/<pid>/cwd`, walk
ppids) -- the 17-calls-before-the-first-(d) cost this claim cites.

### What landed (`extensions/agi/bin/verification.py`)

- `PROC = Path("/proc")` -- a module constant, so a test can hand the whole
  process table to a fake (a non-Linux box has no `/proc`).
- `_lock_chain(pid)` -- the pid and up to FOUR ppid hops, `PPid:` read from
  `PROC/<pid>/status`, stopping at 0, a repeat, or an unreadable entry.
- `_lock_tree(groot, pid)` -- `readlink PROC/<pid>/cwd`, resolved against
  `locations.git_common_root(groot)`: under `<main>/.agi/worktrees/<name>` ->
  `<name>`; under MAIN -> `main`; elsewhere its basename; unreadable ->
  `unresolved`.
- `_lock_runner(groot, chain)` -- the first pid on the chain matching a LIVE
  lease's `agent_pid`/`holder_pid`, formatted
  ` runner <agent_id> tier=<tier> iter=<iter>`.
- `render_window`'s live-holder branch prints ONE line in the required shape:
  `lock: held by <pid> since <HH:MM:SSZ> (age <N>s, tree <t>, cmd <head60>)`,
  with the runner clause appended when one matches. `age` is
  `int(time.time() - lock_path.stat().st_mtime)`; `cmd` is the first 60 bytes
  of `PROC/<pid>/cmdline` with NULs as spaces. Both read failures degrade to
  `unresolved` -- no exception escapes.

The free branch is untouched: `lines.append("lock: free")` is unchanged and
is asserted byte-for-byte.

### What landed (`extensions/agi/bin/spawn_budget.py`)

- `live_leases_readonly(root)` -- live lease rows, READ-ONLY: no sweep, no
  unlink, no lock. The sibling of `live_iteration_ids`, for a reader that must
  carry `agent_id`/`tier`/`iter`. `verification.py` imports `spawn_budget` and
  calls THIS -- there is no second glob/parse of the budget dir anywhere in
  `verification.py`.

## Evidence

Live read on this tree (a real holder in this seat's worktree, no fixture):

```
POST-FIX held line: lock: held by 1177450 since 19:04:54Z (age 0s, tree a00-09301626, cmd /bin/bash -c cd /home/ubuntu/work/agi/.agi/worktrees/a00-093)
POST-FIX free line: lock: free
```

`tree a00-09301626` is the real worktree name and the cmd head is a real 60
byte cut -- the conjuncts are live, not only fixture-true.

Tests (`extensions/agi/tests/test_verification_window.py`, +4):

```
$ python3 -m pytest extensions/agi/tests/test_verification_window.py -q
.........                                                                [100%]
9 passed in 0.20s
```

1. `..._names_tree_age_and_command_of_a_worktree_holder` -- fake `PROC` whose
   `<pid>/cwd` is inside `.agi/worktrees/a00-cafe1234`: asserts
   `tree a00-cafe1234`, `age \d+s`, and the cmdline head on the lock line.
2. `..._names_main_when_the_holder_sits_in_the_main_checkout` -- `tree main`.
3. `..._names_the_registered_runner_behind_the_holder` -- a live lease written
   at `spawn_budget.budget_dir(groot)` with `agent_pid` one ppid hop above the
   holder: asserts `runner a00-deadbeef123456 tier=kid iter=7`.
4. `..._lock_line_degrades_and_free_is_byte_identical` -- an EMPTY fake `PROC`:
   no exception, `tree unresolved`, `cmd unresolved`; and a fresh free fixture
   yields exactly `["lock: free"]`.

No test depends on this box's real `/proc` or on a spawned process; the two
live values above are extra, not the evidence.

Neighbouring modules that cover the touched files:

```
$ python3 -m pytest extensions/agi/tests/test_verification_window.py \
    extensions/agi/tests/test_verification.py \
    extensions/agi/tests/test_verify_unified.py \
    extensions/agi/tests/test_verify_suite_record.py \
    extensions/agi/tests/test_verification_manifest.py \
    extensions/agi/tests/test_verification_seat_model.py \
    extensions/agi/tests/test_verification_kept_merge.py \
    extensions/agi/tests/test_spawn_budget.py -q
166 passed in 7.61s
```

Production lines, measured once with `git diff --numstat` over the two
production paths the brief named (test file excluded): 61 + 5 added, 4
removed = **66 added / 62 net** against a ceiling of 35. Above the ceiling,
below the 2x stop gate (70) -- the count is recorded in `production_lines`
and no re-brief is requested.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
This version carries the PARENT review of the kid's landed bytes (kid a00-6da6a81b; its own reasoning, summarised rather than appended: the four conjuncts each need their own /proc read plus a degrade arm -- chain walk, tree resolution, cmd head, runner lookup -- which is why the change is 66 added production lines against a 35 ceiling, below the 2x stop gate (70); _lock_runner reads the lease rows before walking the chain, forced because the match cannot be decided without the rows; iter=None renders as 'iter=None' rather than an invented value).

WHAT I REVIEWED: the diff at commit e4b5a0320 (git diff of verification.py + spawn_budget.py + the test module), not the kid's result file. render_window's live-holder branch now appends '(age <N>s, tree <t>, cmd <head60>)' and a ' runner <agent_id> tier=<t> iter=<i>' clause; spawn_budget gained live_leases_readonly() and verification imports it, so there is no second glob of the budget dir.

WHAT I RAN (parent-run, in scratch, one negative probe per conjunct, using the REAL /proc rather than the kid's fake): a live `sleep 120` with cwd inside .agi/worktrees/post-foo -> 'age 42s, tree post-foo, cmd sleep 120' on exactly ONE lock line; monkeypatching spawn_budget.live_leases_readonly to return one fabricated row -> that row surfaces on the line (the call site reaches the changed bytes), while a lease whose pids are DEAD is not named; pid 2 (alive, /proc/2/cwd EACCES) -> 'tree unresolved' with no traceback and pid 999999999 -> 'lock: free'; the free line is exactly ['lock: free'] and gains no age/tree/cmd token. All nine probe assertions pass, and none of them can pass on the pre-fix bytes (the tokens and the reader do not exist there).

VERDICT KEPT: proved. The one thing I am NOT certifying: the worktree spelling is hardcoded as '<main>/.agi/worktrees/' via os.path.join, so a graph root that IS the repo root (the legacy layout) would mis-spell the worktree branch -- unreachable in this repo, named here rather than left silent.
<!-- THOUGHT:END -->

## Agent Notes
Built the four conjuncts on the real bytes: render_window's live-holder line now carries pid, age (lock mtime), tree (git_common_root + /proc/<pid>/cwd -> worktree name | main | unresolved) and the 60-byte cmdline head, plus a runner clause from a new read-only spawn_budget.live_leases_readonly() over the holder's 4-hop ppid chain; every /proc read degrades to 'unresolved' and lock: free is byte-identical. 4 new fake-/proc tests in test_verification_window.py (9 passed) + 166 passed across the 8 modules covering the two touched files. 66 production lines vs the 35 ceiling, below the 2x gate -- recorded in production_lines.

PARENT REVIEW (a00-09301626): reviewed the diff at e4b5a0320; ran 4 parent-run negative probes on the REAL /proc (one per conjunct: live-worktree holder names pid/age/tree/cmd on one line; the runner row surfaces through spawn_budget.live_leases_readonly and a DEAD lease is not named; unreadable /proc -> 'unresolved' with no traceback and dead pid -> free; free line byte-identical). All pass; verdict went out proved with evidence_runs=[experiment:a00-6da6a81b-f10a71]. Overage recorded, not hidden: 66 production lines vs the 35 ceiling (below the 2x stop gate of 70 -- no re-brief), disclosed by the kid as production_lines=66. Residual, not a blocker: the worktree branch spells '<main>/.agi/worktrees/' by construction, which is the non-legacy layout only.
